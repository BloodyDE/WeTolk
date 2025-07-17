from django.contrib import admin
from .models import Ticket, TicketComment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title", "creator_name", "role", "category",
        "subcategory", "type", "project", "project_type",
        "created_at",
    )
    list_filter = (
        "role", "category", "subcategory",
        "type", "project", "project_type",
    )
    search_fields = ("title", "creator_name", "tags")
    inlines = []

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    fields = ("author_name", "message", "created_at")
    readonly_fields = ("author_name", "message", "created_at")
    extra = 0

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author_name", "created_at")
    list_filter = ("author_name",)
    search_fields = ("author_name", "message")
