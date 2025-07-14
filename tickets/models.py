from django.db import models
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class Ticket(models.Model):
    title = models.CharField(max_length=200)

    # 1) Deine Choice-Listen – jede Zeile ein (Value, Label)-Tupel
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
        ('Bug',     'Bug'),
        ('Feature', 'Feature'),
        ('Task',    'Task'),
    ]
    PROJECT_CHOICES = [
        ('Sonne', 'Sonne'),
    ]
    PROJECT_TYPE_CHOICES = [
        ('Forschungsschiff', 'Forschungsschiff'),
    ]
    #Für mehr Optionen einfach ('Elektroingenieur', 'Elektroingenieur') hinzufügen#

    # 2) Felder mit choices=…  –  Django rendert dann automatisch <select>…
    role         = models.CharField(
                       max_length=50,
                       choices=ROLE_CHOICES,
                       default='Architekt'
                   )
    category     = models.CharField(
                       max_length=50,
                       choices=CATEGORY_CHOICES,
                       default='Projektmanagement'
                   )
    subcategory  = models.CharField(
                       max_length=50,
                       choices=SUBCATEGORY_CHOICES,
                       default='Kommunikation'
                   )
    type         = models.CharField(
                       max_length=50,
                       choices=TYPE_CHOICES,
                       default='Task'
                   )
    project      = models.CharField(
                       max_length=50,
                       choices=PROJECT_CHOICES,
                       default='Sonne'
                   )
    project_type = models.CharField(
                       max_length=50,
                       choices=PROJECT_TYPE_CHOICES,
                       default='Forschungsschiff'
                   )

    tags        = models.CharField(
                     max_length=255,
                     blank=True,
                     help_text="Komma-separierte Schlagworte"
                  )
    description = models.TextField()
    solution    = models.TextField(blank=True)
    impact      = models.TextField(blank=True)
    attachment  = models.FileField(upload_to="attachments/", blank=True, null=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",")]


class TicketComment(models.Model):
    ticket      = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    message     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kommentar von {self.created_by} am {self.created_at:%d.%m.%Y}"

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title', 'role', 'category', 'subcategory',
            'type', 'project', 'project_type',
            'tags', 'description', 'solution', 'impact', 'attachment'
        ]
        widgets = {
            'role':         forms.Select(),
            'category':     forms.Select(),
            'subcategory':  forms.Select(),
            'type':         forms.Select(),
            'project':      forms.Select(),
            'project_type': forms.Select(),
        }