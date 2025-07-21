# tickets/urls.py

from django.urls import path
from . import views
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    ticket_snippet,
    preview_bullet,
    
)

app_name = "tickets"

urlpatterns = [
    # Übersicht aller Knowledges unter "/"
    path(
        "",
        TicketListView.as_view(),
        name="ticket_list"
    ),

    # Formular zum Erstellen eines neuen Knowledges unter "/create/"
    path(
        "create/",
        TicketCreateView.as_view(),
        name="ticket_create"
    ),

    # HTMX-Snippet: lädt Detailansicht in einen Ausschnitt unter "/snippet/<pk>/"
    path(
        "snippet/<int:pk>/",
        ticket_snippet,
        name="ticket_snippet"
    ),

    # Volle Detailseite (Fallback), z.B. für direkten Link "/<pk>/"
    path(
        "<int:pk>/",
        TicketDetailView.as_view(),
        name="ticket_detail"
    ),

    # HTMX‑Endpoint für Live‑Bullet‑Preview unter "/preview/"
    path(
        "preview/",
        preview_bullet,
        name="preview_bullet"
    ),
    
    path(
        'datenschutz/', views.PrivacyView.as_view(), name='privacy'),
]
