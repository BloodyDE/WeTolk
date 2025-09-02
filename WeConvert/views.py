from django.shortcuts import render
from django.http import FileResponse, HttpResponseBadRequest
from .forms import ImageUploadForm
from PIL import Image
import io
import os

def convert_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest("Ungültiges Formular")

        uploaded = form.cleaned_data["image"]
        base, _ = os.path.splitext(uploaded.name)

        # NEU: optionale Parameter (fallen zurück auf Standardwerte)
        out_format = (form.cleaned_data.get("out_format") or "PNG").upper()     # PNG | JPEG | WEBP
        quality = form.cleaned_data.get("quality")
        try:
            quality = int(quality) if quality is not None else 85               # 1..100, Default 85
        except (TypeError, ValueError):
            quality = 85
        progressive = bool(form.cleaned_data.get("progressive"))                # nur JPEG sinnvoll
        lossless_webp = bool(form.cleaned_data.get("lossless_webp"))            # nur WEBP

        try:
            img = Image.open(uploaded)
            buf = io.BytesIO()

            if out_format == "PNG":
                # PNG hat keinen "quality"-Begriff, sondern compress_level 0..9.
                # Mapping: quality 1..100 -> compress_level 9..0 (höhere Qualität = weniger Kompression)
                compress_level = int(round((100 - max(1, min(100, quality))) * 9 / 99))
                compress_level = max(0, min(9, compress_level))
                img.convert("RGBA").save(buf, format="PNG", optimize=True, compress_level=compress_level)
                ext = "png"
                ctype = "image/png"

            elif out_format == "JPEG":
                q = max(1, min(95, int(quality)))  # >95 bringt kaum was, Dateigröße wächst stark
                img.convert("RGB").save(buf, format="JPEG", quality=q, optimize=True, progressive=progressive)
                ext = "jpg"
                ctype = "image/jpeg"

            elif out_format == "WEBP":
                if lossless_webp:
                    img.save(buf, format="WEBP", lossless=True, method=6)
                else:
                    q = max(1, min(100, int(quality)))
                    img.save(buf, format="WEBP", quality=q, method=6)
                ext = "webp"
                ctype = "image/webp"

            else:
                # Fallback: verhalte dich wie vorher (PNG)
                img.convert("RGBA").save(buf, format="PNG", optimize=True)
                ext = "png"
                ctype = "image/png"

            buf.seek(0)
        except Exception:
            return HttpResponseBadRequest("Datei konnte nicht konvertiert werden.")

        filename = f"{base}_converted.{ext}"

        # Response + Cookie wie bisher
        response = FileResponse(buf, as_attachment=True, filename=filename, content_type=ctype)
        response.set_cookie("weconvert_done", "1", max_age=60, samesite="Lax", path="/")
        return response

    # GET: Formular anzeigen
    return render(request, "weconvert/upload.html", {"form": ImageUploadForm()})
