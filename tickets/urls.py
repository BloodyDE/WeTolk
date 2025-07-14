# tickets/urls.py
from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("list/", views.TicketListView.as_view(), name="ticket_list"),
    path("create/", views.TicketCreateView.as_view(), name="ticket_create"),
    path("snippet/<int:pk>/", views.ticket_snippet, name="ticket_snippet"),
    # optional: full detail als Fallback
    path("<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("", views.TicketCreateView.as_view(), name="ticket_create"),
]