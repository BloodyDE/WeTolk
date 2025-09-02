from django.urls import path
from .views import (
    TicketListView, TicketCreateView, TicketDetailView,
    ticket_snippet, preview_bullet,
    PrivacyView, DownloadPasswordView, DownloadDBView, HomeView,
)

app_name = "tickets"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),                     # /  (Home wie am Anfang)
    path("list/", TicketListView.as_view(), name="ticket_list"),   # /list/  (Alle Knowledges)
    path("new/", TicketCreateView.as_view(), name="ticket_new"),   # /new/
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),  # /<id>/
    path("<int:pk>/snippet/", ticket_snippet, name="ticket_snippet"),
    path("preview-bullet/", preview_bullet, name="preview_bullet"),
    path("datenschutz/", PrivacyView.as_view(), name="privacy"),
    path("download/", DownloadPasswordView.as_view(), name="ticket_download_pass"),
    path("download/db/", DownloadDBView.as_view(), name="ticket_download_db"),
]