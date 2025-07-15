from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = [
            'creator_name',  # unbedingt hier aufnehmen!
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
            'creator_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': '(Pflichtfeld)',
            }),
            'role':         forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'category':     forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'subcategory':  forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'type':         forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'project':      forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'project_type': forms.Select(attrs={'class': 'p-2 border rounded w-full'}),
            'tags':         forms.HiddenInput(),
            'description':  forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
            'solution':     forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
            'impact':       forms.Textarea(attrs={'class': 'p-2 border rounded w-full h-32'}),
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