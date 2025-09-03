from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = [
            "creator_name",
            "title",
            "role",
            "category",
            "subcategory",
            "type",
            "project",
            "project_type",
            "tags",
            "description",
            "solution",
            "impact",
            "attachment",
        ]
        labels = {
            "creator_name": "Name des Erstellers",
            "title":        "Titel",
            "role":         "Rolle",
            "category":     "Kategorie",
            "subcategory":  "Unterkategorie",
            "type":         "Art",
            "project":      "Projekt",
            "project_type": "Projektart",
            "tags":         "Schlagworte",
            "description":  "Beschreibung",
            "solution":     "Lösung",
            "impact":       "Auswirkung",
            "attachment":   "Anhang",
        }
        widgets = {
            # ✅ Widget statt Field:
            "creator_name": forms.TextInput(attrs={
                "placeholder": "Anonym",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
                "autocomplete": "name",
            }),
            "title": forms.TextInput(attrs={
                "placeholder": "Kurzen, aussagekräftigen Titel eingeben",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
            }),
            "tags": forms.TextInput(attrs={
                "placeholder": "Schlagworte mit Komma trennen, z. B. bug, ui, backend",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
            }),
            "role":         forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "category":     forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "subcategory":  forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "project":      forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "project_type": forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "type":         forms.Select(attrs={"class": "w-full p-3 rounded border border-gray-300 bg-white/75 focus:ring-2 focus:ring-indigo-200 transition"}),
            "description":  forms.Textarea(attrs={
                "placeholder": "Problem hier beschreiben… ",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4,
            }),
            "solution":     forms.Textarea(attrs={
                "placeholder": "Lösungsidee hier skizzieren… ",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4,
            }),
            "impact":       forms.Textarea(attrs={
                "placeholder": "Auswirkungen erläutern… ",
                "class": "w-full p-3 rounded border border-gray-300 bg-white/75 "
                         "focus:ring-2 focus:ring-indigo-200 transition",
                "rows": 4,
            }),
            "attachment":   forms.ClearableFileInput(attrs={"class": "mt-2"}),
        }

    # ✅ In der Form, nicht top-level:
    def clean_creator_name(self):
        name = (self.cleaned_data.get("creator_name") or "").strip()
        return name or "Anonym"


class CommentForm(forms.ModelForm):
    class Meta:
        model  = TicketComment
        fields = ["author_name", "message"]
        labels = {
            "author_name": "Name (optional)",
            "message":     "Kommentar",
        }
        widgets = {
            "author_name": forms.TextInput(attrs={
                "placeholder": "Anonym",
                "class": "w-full p-2 border rounded focus:ring-2 focus:ring-indigo-200",
                "autocomplete": "name",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Schreib deinen Kommentar…",
                "rows": 3,
                "class": "w-full p-2 border rounded focus:ring-2 focus:ring-indigo-200",
            }),
        }

    def clean_author_name(self):
        return (self.cleaned_data.get("author_name") or "").strip() or "Anonym"