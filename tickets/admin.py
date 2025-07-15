from django.contrib import admin
from .models import Ticket, TicketComment

class TicketCommentInline(admin.TabularInline):
    """
    Kommentare direkt im Ticket‑Admin als Inline bearbeiten.
    """
    model = TicketComment
    extra = 0
    readonly_fields = ("created_by", "created_at")
    can_delete = False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin‑Interface für Tickets.
    """
    list_display = (
        "title",
        "creator_name",
        "role",
        "category",
        "subcategory",
        "type",
        "project",
        "project_type",
        "created_at",
    )
    list_filter = (
        "role",
        "category",
        "subcategory",
        "type",
        "project",
        "project_type",
    )
    search_fields = ("title", "creator_name", "tags")
    ordering = ("-created_at",)
    inlines = [TicketCommentInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    """
    Admin‑Interface für Ticket‑Kommentare.
    """
    list_display = ("ticket", "created_by", "created_at")
    list_filter = ("created_by",)
    search_fields = ("message",)
    ordering = ("-created_at",)
