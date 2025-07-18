from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = [
            'creator_name',  
            'title',
            'role',
            'category',
            'subcategory',
            'type',
            'project',
            'project_type',
            'tags',
            'description',
            'solution',
            'impact',
            'attachment',
        ]
        labels = {
            'creator_name': 'Name des Erstellers',
            'title':        'Titel',
            'role':         'Rolle',
            'category':     'Kategorie',
            'subcategory':  'Unterkategorie',
            'type':         'Art',
            'project':      'Projekt',
            'project_type': 'Projektart',
            'tags':         'Schlagworte',
            'description':  'Beschreibung',
            'solution':     'Lösung',
            'impact':       'Auswirkung',
            'attachment':   'Anhang',
        }
        widgets = {
            "creator_name": forms.TextInput(attrs={
                "placeholder": "z. B. Max Mustermann",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"
            }),
            "title": forms.TextInput(attrs={
                "placeholder": "Kurzen, aussagekräftigen Titel eingeben",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"
            }),
            "tags": forms.TextInput(attrs={
                "placeholder": "Schlagworte mit Komma trennen, z. B. bug, ui, backend",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"
            }),

            # Dropdowns bleiben Select (keine placeholder)
            "role": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "category": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "subcategory": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "project": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "project_type": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "type": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),

            # Textareas mit Placeholder
            "description": forms.Textarea(attrs={
                "placeholder": "Problem hier beschreiben… Enter Drücken für Bulletpoints",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4
            }),
            "solution": forms.Textarea(attrs={
                "placeholder": "Lösungsidee hier skizzieren… Enter Drücken für Bulletpoints",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4
            }),
            "impact": forms.Textarea(attrs={
                "placeholder": "Auswirkungen erläutern… Enter Drücken für Bulletpoints",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4
            }),

            # Attachment bleibt ClearableFileInput
            "attachment": forms.ClearableFileInput(attrs={"class": "mt-2"}),
        }

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        required=False,
        label="Name (optional)",
        widget=forms.TextInput(attrs={
            "placeholder": "Dein Name (leer für ‚Anonym‘)",
            "class": "w-full p-2 border rounded focus:ring-2 focus:ring-indigo-200"
        })
    )

    class Meta:
        model  = TicketComment
        fields = ["author_name", "message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "placeholder": "Hier deinen Kommentar eingeben…",
                "class": "w-full p-2 border rounded focus:ring-2 focus:ring-indigo-200",
                "rows": 4,
            }),
        }