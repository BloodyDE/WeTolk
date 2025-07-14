from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .models import Ticket
from .forms import TicketForm, CommentForm

class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"
    # Nach erfolgreichem Abspeichern direkt zur Liste weiterleiten:
    success_url = reverse_lazy("tickets:ticket_list")

    def form_valid(self, form):
        # Setze das Feld created_by automatisch auf den angemeldeten User
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TicketListView(ListView):
    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Baum-Struktur für Kategorie → Unterkategorie
        tree = {}
        for t in ctx["object_list"]:
            tree.setdefault(t.category, {}) \
                .setdefault(t.subcategory, []) \
                .append(t)
        ctx["ticket_tree"] = tree
        return ctx


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


def ticket_snippet(request, pk):
    """
    HTMX-Snippet: Lädt nur den Detail-Ausschnitt für #detail-pane.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    comment_form = CommentForm()
    return render(request, "tickets/ticket_snippet.html", {
        "ticket": ticket,
        "comment_form": comment_form,
    })
