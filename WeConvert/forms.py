from django import forms
from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Bild")

    out_format = forms.ChoiceField(
        label="Zielformat",
        choices=[
            ("PNG",  "PNG (.png)"),
            ("JPEG", "JPEG (.jpg)"),
            ("WEBP", "WebP (.webp)"),
        ],
        initial="PNG",
        required=False,
    )

    quality = forms.IntegerField(
        label="Qualität",
        min_value=1,
        max_value=100,
        initial=85,
        required=False,
        widget=forms.NumberInput(attrs={
            "type": "range",
            "min": "1",
            "max": "100",
            "step": "1",
        }),
        help_text="Höher = bessere Qualität, größere Datei.",
    )

    progressive = forms.BooleanField(
        label="Progressive JPEG",
        required=False,
        initial=True,
    )

    lossless_webp = forms.BooleanField(
        label="WebP lossless (ignoriert Qualität)",
        required=False,
        initial=False,
    )