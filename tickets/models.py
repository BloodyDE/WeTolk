from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    ROLE_CHOICES = [
        ('Teilprojektleiter', 'Teilprojektleiter'),
        ('Projektingenieur', 'Projektingenieur'),
        ('Controller', 'Controller'),
    ]

    CATEGORY_CHOICES = [
        ('Beleuchtungssysteme', 'Beleuchtungssysteme (SNE3)'),
        ('Kabelanlage', 'Kabelanlage'),
        ('Automation', 'Automation'),
        ('ILS', 'ILS'),
    ]

    SUBCATEGORY_CHOICES = [
        ('Beleuchtungstreiber', 'Beleuchtungstreiber'),
        ('Leuchten', 'Leuchten'),
        ('Kabelschirmung', 'Kabelschirmung'),
        ('Kabelbahn', 'Kabelbahn'),
        ('BUS-Systeme', 'BUS-Systeme'),
        ('SPS/DPU', 'SPS/DPU'),
        ('Sparepart Analysis', 'Sparepart Analysis'),
        ('Logistic-Support Analysis', 'Logistic-Support Analysis'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('Offshore', 'Offshore'),
        ('Militär', 'Militär'),
        ('Forschungsschiff', 'Forschungsschiff'),
        ('Zivil', 'Zivil und sonstiges'),
    ]

    PROJECT_CHOICES = [
        ('Elia MOG', 'Elia MOG'),
        ('METEOR', 'METEOR'),
    ]

    TYPE_CHOICES = [
        ('Material', 'Material'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Sicherheit', 'Sicherheit'),
    ]

    creator_name = models.CharField(
        max_length=100,
        verbose_name="Name des Erstellers",
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titel",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='Teilprojektleiter',
        verbose_name="Rolle",
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Beleuchtungssysteme',
        verbose_name="Kategorie",
    )
    subcategory = models.CharField(
        max_length=50,
        choices=SUBCATEGORY_CHOICES,
        default='Leuchten',
        verbose_name="Unterkategorie",
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='Material',
        verbose_name="Art",
    )
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        default='Offshore',
        verbose_name="Projektart",
    )
    project = models.CharField(
        max_length=50,
        choices=PROJECT_CHOICES,
        default='Elia MOG',
        verbose_name="Projekt",
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Komma-separierte Schlagworte",
        verbose_name="Schlagworte",
    )
    description = models.TextField(verbose_name="Beschreibung")
    solution = models.TextField(blank=True, verbose_name="Lösung")
    impact = models.TextField(blank=True, verbose_name="Auswirkung")
    attachment = models.FileField(
        upload_to="attachments/",
        blank=True,
        null=True,
        verbose_name="Anhang",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return self.title or f"Ticket {self.pk}"

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",")]

class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ticket",
    )
    author_name = models.CharField(
        max_length=100,
        default="Anonym",
        help_text="Dein Name oder leer lassen für ‚Anonym‘",
    )
    message = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return f"{self.author_name} on {self.ticket.title}"