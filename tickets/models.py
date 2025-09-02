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

    # Erweiterte Liste gültiger Projekte
    PROJECT_CHOICES = [
        ('BC Ferries', 'BC Ferries'),
        ('METEOR', 'METEOR'),
        ('Walther Herwig', 'Walther Herwig'),
        ('Sonne', 'Sonne'),
        ('F126', 'F126'),
        ('MEKO Brasilien', 'MEKO Brasilien'),
        ('ELIAMOG', 'ELIAMOG'),
    ]

    TYPE_CHOICES = [
        ('Material', 'Material'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Sicherheit', 'Sicherheit'),
    ]

    creator_name = models.CharField(
        "Name des Erstellers",
        max_length=100,
        blank=True,
        null=False,  # kein Null in der DB
        help_text='Leer lassen für „Anonym“',
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
        default='METEOR',
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
        Ticket, on_delete=models.CASCADE, related_name="comments", verbose_name="Ticket"
    )
    author_name = models.CharField(
        max_length=100,
        blank=True,                 # <— wichtig
        default="",                 # speichere ggf. leer und setze unten auf "Anonym"
        help_text="Dein Name oder leer lassen für 'Anonym'",
    )
    message = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")


    def save(self, *args, **kwargs):
        # Nur beim Speichern befüllen, wenn leer/Whitespace
        self.creator_name = (self.creator_name or "").strip() or "Anonym"
        super().save(*args, **kwargs)

    def __str__(self):
        ticket_title = self.ticket.title or f"Ticket {self.ticket_id}"
        return f"{self.author_name or 'Anonym'} on {ticket_title}"