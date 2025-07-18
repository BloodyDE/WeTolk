from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST

from .models import Ticket, TicketComment
from .forms import TicketForm, CommentForm


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("tickets:ticket_list")


class TicketListView(ListView):
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "ticket_list"

    def get_queryset(self):
        qs = super().get_queryset().order_by('category', 'subcategory', 'created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(tags__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Baumstruktur erstellen
        tree = {}
        for t in ctx['object_list']:
            tree.setdefault(t.category, {}) \
                .setdefault(t.subcategory, []) \
                .append(t)
        ctx['ticket_tree'] = tree
        # Suchbegriff zurückgeben
        ctx['query'] = self.request.GET.get('q', '')
        # Erstes Ticket und CommentForm für Detail-Pane
        first = ctx['object_list'].first() if hasattr(ctx['object_list'], 'first') else (
            ctx['object_list'][0] if ctx['object_list'] else None
        )
        ctx['initial_ticket'] = first
        ctx['comment_form'] = CommentForm()
        return ctx


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx


from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def ticket_snippet(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if not comment.author_name.strip():
                comment.author_name = "Anonym"
            comment.ticket = ticket
            comment.save()
        # Nach POST weiterhin das aktualisierte Snippet zurückgeben
    else:
        form = CommentForm()
    return render(request, "tickets/ticket_snippet.html", {
        "ticket": ticket,
        "comment_form": form,
    })

@require_POST
def preview_bullet(request):
    text = request.POST.get('text', '')
    if not text.strip():
        return HttpResponseBadRequest('Kein Text übergeben.')
    return render(request, 'tickets/_bullet_list.html', {'text': text})