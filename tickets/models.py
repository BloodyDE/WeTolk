# tickets/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    creator_name = models.CharField(
        max_length=100,
        verbose_name="Name des Erstellers",
        help_text="Bitte hier Deinen Namen eingeben",
    )
    title = models.CharField(max_length=200, verbose_name="Titel")

    # Choice‑Listen
    ROLE_CHOICES = [
        ('Architekt',        'Architekt'),
        ('Elektroingenieur', 'Elektroingenieur'),
    ]
    CATEGORY_CHOICES = [
        ('Projektmanagement', 'Projektmanagement'),
    ]
    SUBCATEGORY_CHOICES = [
        ('Kommunikation',     'Kommunikation'),
    ]
    TYPE_CHOICES = [
        ('Organisatorisch',     'Organisatorisch'),
    ]
    PROJECT_CHOICES = [
        ('Sonne', 'Sonne'),
    ]
    PROJECT_TYPE_CHOICES = [
        ('Forschungsschiff', 'Forschungsschiff'),
    ]

    role         = models.CharField(
                       max_length=50,
                       choices=ROLE_CHOICES,
                       default='Architekt',
                       verbose_name="Rolle"
                   )
    category     = models.CharField(
                       max_length=50,
                       choices=CATEGORY_CHOICES,
                       default='Projektmanagement',
                       verbose_name="Kategorie"
                   )
    subcategory  = models.CharField(
                       max_length=50,
                       choices=SUBCATEGORY_CHOICES,
                       default='Kommunikation',
                       verbose_name="Unterkategorie"
                   )
    type         = models.CharField(
                       max_length=50,
                       choices=TYPE_CHOICES,
                       default='Task',
                       verbose_name="Art"
                   )
    project      = models.CharField(
                       max_length=50,
                       choices=PROJECT_CHOICES,
                       default='Sonne',
                       verbose_name="Projekt"
                   )
    project_type = models.CharField(
                       max_length=50,
                       choices=PROJECT_TYPE_CHOICES,
                       default='Forschungsschiff',
                       verbose_name="Projektart"
                   )

    tags        = models.CharField(
                     max_length=255,
                     blank=True,
                     help_text="Komma‑separierte Schlagworte",
                     verbose_name="Schlagworte"
                  )
    description = models.TextField(verbose_name="Beschreibung")
    solution    = models.TextField(blank=True, verbose_name="Lösung")
    impact      = models.TextField(blank=True, verbose_name="Auswirkung")
    attachment  = models.FileField(
                     upload_to="attachments/",
                     blank=True,
                     null=True,
                     verbose_name="Anhang"
                  )
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        """
        Gibt die Schlagworte als Liste zurück.
        """
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",")]


class TicketComment(models.Model):
    ticket     = models.ForeignKey(
                     Ticket,
                     on_delete=models.CASCADE,
                     related_name="comments",
                     verbose_name="Ticket"
                 )
    created_by = models.ForeignKey(
                     User,
                     on_delete=models.CASCADE,
                     verbose_name="Kommentar von"
                 )
    message    = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return f"Kommentar von {self.created_by} am {self.created_at:%d.%m.%Y}"
