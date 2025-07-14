# tickets/forms.py

from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'role',
            'category',
            'subcategory',
            'project',
            'project_type',
            'tags',
            'description',
            'solution',
            'impact',
            'attachment',
        ]
        
        labels = {
            'title': 'Titel',
            'role': 'Rolle',
            'category': 'Kategorie',
            'subcategory': 'Unterkategorie',
            'project': 'Projekt',
            'project_type': 'Projektart',
            'tags': 'Schlagworte',
            'description': 'Beschreibung',
            'solution': 'Lösung',
            'impact': 'Auswirkung',
            'attachment': 'Anhang',
        }

        widgets = {
            'role':         forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'category':     forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'subcategory':  forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'type':         forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'project':      forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'project_type': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'description':  forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
            'solution':     forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
            'impact':       forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
            # 'attachment' bleibt Default-Widget
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model  = TicketComment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "p-2 border rounded w-full h-24 focus:ring-4 focus:ring-indigo-200"
            }),
        }
