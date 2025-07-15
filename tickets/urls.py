from django.urls import path
from . import views
from .views import preview_bullet

app_name = "tickets"

urlpatterns = [
    # Root → Liste aller Knowledges
    path("", views.TicketListView.as_view(),   name="ticket_list"),

    # Create-Form unter /create/
    path("create/", views.TicketCreateView.as_view(), name="ticket_create"),

    # HTMX-Snippet
    path("snippet/<int:pk>/", views.ticket_snippet, name="ticket_snippet"),

    # Vollständige Detail-Seite (optional)
    path("<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),

    # _bullet_list.html-Snippet für HTMX-Vorschau
    path("preview/", preview_bullet, name="preview_bullet"),
    ]
