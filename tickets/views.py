# tickets/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST

from .models import Ticket
from .forms import TicketForm, CommentForm


class TicketCreateView(CreateView):
    """
    Zeigt das Formular zum Anlegen eines neuen Tickets und speichert es ab.
    """
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("tickets:ticket_list")


class TicketListView(ListView):
    """
    Zeigt alle Tickets in einer Baum‑Ansicht nach Kategorie → Unterkategorie.
    """
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "ticket_list"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tree = {}
        for t in ctx["object_list"]:
            tree.setdefault(t.category, {}) \
                .setdefault(t.subcategory, []) \
                .append(t)
        ctx["ticket_tree"] = tree
        return ctx


class TicketDetailView(DetailView):
    """
    Detailansicht für ein einzelnes Ticket (Fallback, wenn kein HTMX‑Snippet verwendet wird).
    """
    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


def ticket_snippet(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.created_by = request.user
            comment.save()
        # nach dem Speichern den aktualisierten Kommentar‑Snippet zurückliefern
    else:
        form = CommentForm()
    return render(request, "tickets/ticket_snippet.html", {
        "ticket": ticket,
        "comment_form": form,
    })


@require_POST
def preview_bullet(request):
    """
    HTMX‑Endpoint: Nimmt im POST‑Body das Feld 'text' und
    rendert daraus eine ul.list-disc via _bullet_list.html.
    """
    text = request.POST.get("text", "")
    if not text.strip():
        return HttpResponseBadRequest("Kein Text übergeben.")
    return render(request, "tickets/_bullet_list.html", {"text": text})
