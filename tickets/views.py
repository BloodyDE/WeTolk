from __future__ import annotations
from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q, Count, Min, F
from django.db.models.expressions import Func
from django.db.models.functions import Lower
from django.http import (
    FileResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic.edit import FormMixin
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
)

import os
import secrets

from .forms import CommentForm, TicketForm
from .models import Ticket, TicketComment


# ---------- DB helpers ----------
class Trim(Func):
    """Portable TRIM() for SQLite/Postgres."""
    function = "TRIM"
    arity = 1


# ---------- Create ----------
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("tickets:ticket_list")

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        # Cancel aus der Vorschau → Tempdatei löschen
        if "cancel" in request.POST:
            tmp_id = request.POST.get("attachment_tmp_id")
            if tmp_id:
                try:
                    default_storage.delete(tmp_id)
                except Exception:
                    pass
            return redirect(request.path)

        if not form.is_valid():
            return self.form_invalid(form)

        # "Fertig" → speichern
        if "confirm" in request.POST:
            obj = form.save(commit=False)

            # 1) neuer Anhang in diesem Request?
            uploaded = request.FILES.get("attachment")
            if uploaded:
                obj.attachment = uploaded
            else:
                # 2) Tempdatei übernehmen
                tmp_id = request.POST.get("attachment_tmp_id")
                if tmp_id and default_storage.exists(tmp_id):
                    orig_name = os.path.basename(tmp_id).split("_", 1)[-1]
                    with default_storage.open(tmp_id, "rb") as fh:
                        obj.attachment.save(orig_name, ContentFile(fh.read()), save=False)
                    try:
                        default_storage.delete(tmp_id)
                    except Exception:
                        pass

            obj.save()
            try:
                form.save_m2m()
            except Exception:
                pass

            self.object = obj
            return redirect(self.get_success_url())

        # "Prüfen" → Vorschau rendern
        preview_data = form.cleaned_data.copy()

        # Tags-Liste für Anzeige
        raw_tags = preview_data.get("tags") or ""
        preview_data["tags_list"] = [t.strip() for t in raw_tags.split(",") if t.strip()]

        # Datei: neu hochgeladen oder frühere Temp-ID
        tmp_id: str | None = None
        uploaded = request.FILES.get("attachment")
        if uploaded:
            tmp_id = f"tmp/{secrets.token_hex(8)}_{uploaded.name}"
            default_storage.save(tmp_id, uploaded)
            preview_data["attachment_name"] = uploaded.name
            preview_data["attachment_url"] = default_storage.url(tmp_id)
        else:
            prev_tmp = request.POST.get("attachment_tmp_id")
            if prev_tmp and default_storage.exists(prev_tmp):
                tmp_id = prev_tmp
                preview_data["attachment_name"] = os.path.basename(prev_tmp).split("_", 1)[-1]
                preview_data["attachment_url"] = default_storage.url(prev_tmp)
            else:
                preview_data["attachment_name"] = ""
                preview_data["attachment_url"] = ""

        context = self.get_context_data(
            form=form,
            preview=True,
            preview_data=preview_data,
            attachment_tmp_id=tmp_id,
        )
        return self.render_to_response(context)


# ---------- List ----------
class TicketListView(ListView):
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "ticket_list"

    def get_queryset(self):
        qs = super().get_queryset()

        # 1) Sortierung (?sort=asc|desc)
        sort = self.request.GET.get("sort", "asc")
        direction = "" if sort == "asc" else "-"
        qs = qs.order_by(f"{direction}created_at", Lower("category"), Lower("subcategory"))

        # 2) Suche (Titel/Tags)
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(tags__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Baumstruktur für Template
        tree: dict[str, dict[str, list[Ticket]]] = {}
        for t in ctx["object_list"]:
            tree.setdefault(t.category, {}).setdefault(t.subcategory, []).append(t)
        ctx["ticket_tree"] = tree

        # Filterwerte für die UI
        ctx["query"] = self.request.GET.get("q", "")
        ctx["sort"] = self.request.GET.get("sort", "asc")
        ctx["initial_ticket"] = None
        ctx["comment_form"] = None
        ctx["open_id"] = self.request.GET.get("open")
        return ctx


# ---------- Detail ----------
class TicketDetailView(FormMixin, DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"   # an deinen Dateinamen anpassen
    form_class = CommentForm                       # gleiche Form wie im Snippet

    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'comment_form' not in ctx:
            ctx['comment_form'] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = self.object

            # KEIN Fallback auf eingeloggten User; nur übernehmen, was eingegeben wurde
            provided = form.cleaned_data.get("author_name", "").strip()
            comment.author_name = provided  # bleibt ggf. leer -> Model setzt "Anonym" in save()

            comment.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)

# ---------- HTMX Partial (rechts im Pane) ----------
@require_http_methods(["GET", "POST"])
def ticket_snippet(request, pk):
    """Liefert NUR den Ticket-Ausschnitt (kein base.html) und verarbeitet Kommentare."""
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.save()
            form = CommentForm()  # leeres Formular nach Erfolg
    else:
        form = CommentForm()

    return render(
        request,
        "tickets/ticket_snippet.html",  # <- Template-Name exakt so verwenden
        {"ticket": ticket, "comment_form": form},
    )


# ---------- Sonstiges ----------
@require_POST
def preview_bullet(request):
    text = request.POST.get("text", "")
    if not text.strip():
        return HttpResponseBadRequest("Kein Text übergeben.")
    return render(request, "tickets/_bullet_list.html", {"text": text})


class PrivacyView(TemplateView):
    template_name = "privacy.html"


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        total_tickets = Ticket.objects.count()

        # Leaderboard ohne regex (portabel für SQLite): Namen trimmen, leere/"anonym" filtern
        qs = (
            Ticket.objects
            .exclude(creator_name__isnull=True)
            .annotate(name_trim=Trim(F("creator_name")))
            .exclude(name_trim="")
            .annotate(name_norm=Lower("name_trim"))
            .exclude(name_norm__in=["anonym", "anonymous"])
            .values("name_norm")
            .annotate(total=Count("id"), display=Min("creator_name"))
            .order_by("-total", "display")[:10]
        )

        rows = list(qs)
        for i, r in enumerate(rows, start=1):
            r["rank"] = i
            r["percent"] = int(round((r["total"] / total_tickets) * 100)) if total_tickets else 0

        ctx["leaderboard"] = rows
        ctx["total_tickets"] = total_tickets
        return ctx


# ---------- Downloads ----------
class DownloadPasswordForm(forms.Form):
    password = forms.CharField(
        label="Passwort",
        widget=forms.PasswordInput(attrs={"class": "w-full p-2 border rounded"}),
    )


class DownloadPasswordView(FormView):
    form_class = DownloadPasswordForm
    template_name = "tickets/download_password.html"

    def form_valid(self, form):
        pw = getattr(settings, "DOWNLOAD_PASSWORD", None)
        if pw and form.cleaned_data["password"] == pw:
            self.request.session["download_ok"] = True
            return redirect("tickets:ticket_download_db")
        return self.form_invalid(form)


class DownloadDBView(View):
    """
    Streamt die komplette SQLite-Datenbankdatei als Download.
    Hinweis: Ausgelegt für SQLite-Dateipfade.
    """

    def get(self, request, *args, **kwargs):
        # Passwortschutz via Session
        if not request.session.get("download_ok"):
            return redirect("tickets:ticket_download_pass")

        # Pfad bestimmen
        db_path = getattr(settings, "DOWNLOAD_DB_PATH", None) or settings.DATABASES["default"]["NAME"]

        # Nur SQLite-Dateien zulassen
        engine = settings.DATABASES["default"]["ENGINE"]
        if "sqlite" not in engine:
            return HttpResponseForbidden("Dieser Download ist nur für SQLite-Datenbanken implementiert.")

        try:
            db_path = str(db_path)
            if not os.path.exists(db_path):
                return HttpResponseForbidden(f"Datei nicht gefunden: {db_path}")
        except Exception as e:
            return HttpResponseForbidden(f"Fehler beim Zugriff: {e}")

        response = FileResponse(open(db_path, "rb"), as_attachment=True, filename="tickets_db.sqlite3")

        # Optional: Flag zurücksetzen
        try:
            del request.session["download_ok"]
        except KeyError:
            pass
        return response
