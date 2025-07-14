from django.contrib import admin
from .models import Ticket, TicketComment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    # hier muss created_by stehen, nicht user
    list_display = ("ticket", "created_by", "created_at")
