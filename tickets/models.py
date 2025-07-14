from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    title         = models.CharField(max_length=200)
    role          = models.CharField(max_length=100)
    category      = models.CharField(max_length=100)
    subcategory   = models.CharField(max_length=100)
    type          = models.CharField(max_length=100)
    project       = models.CharField(max_length=100)
    project_type  = models.CharField(max_length=100)
    tags          = models.CharField(
        max_length=255,
        blank=True,
        help_text="Komma-separierte Schlagworte"
    )
    description   = models.TextField()
    solution      = models.TextField(blank=True)
    impact        = models.TextField(blank=True)
    attachment    = models.FileField(upload_to="attachments/", blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        """
        Gibt die tags-Zeichenkette als Liste zurück,
        oder eine leere Liste, falls kein tag gesetzt ist.
        """
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",")]


class TicketComment(models.Model):
    ticket      = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)   # statt `user`
    message   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kommentar von {self.created_by} am {self.created_at:%d.%m.%Y}"
