# WeConvert/views.py
from io import BytesIO
import os
from django.http import FileResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True  # toleranter bei leicht defekten Dateien

@require_POST
def convert_to_png(request):
    f = request.FILES.get('image')
    if not f:
        return HttpResponseBadRequest("No file uploaded.")

    # Formularwerte
    out_format = (request.POST.get('out_format') or '').upper()  # "PNG" | "JPEG" | "WEBP"
    try:
        quality = int(request.POST.get('quality') or 80)
    except ValueError:
        quality = 80
    quality = max(1, min(100, quality))
    progressive = bool(request.POST.get('progressive'))
    lossless_webp = bool(request.POST.get('lossless_webp'))

    # Bild öffnen
    try:
        img = Image.open(f)
    except Exception:
        return HttpResponseBadRequest("Invalid or unsupported image.")

    base, _ = os.path.splitext(f.name)
    out = BytesIO()

    try:
        if out_format == "JPEG" or out_format == "JPG":
            # JPEG hat kein Alpha → nach RGB
            img = img.convert("RGB")
            img.save(out, format="JPEG", quality=min(95, quality), progressive=progressive, optimize=False)
            filename = f"{base}.jpg"
            ctype = "image/jpeg"

        elif out_format == "WEBP":
            if lossless_webp:
                # verlustfrei ignoriert quality
                img.save(out, format="WEBP", lossless=True)
            else:
                img.save(out, format="WEBP", quality=quality, method=4)
            filename = f"{base}.webp"
            ctype = "image/webp"

        else:
            # PNG (Default)
            img = img.convert("RGBA")
            # quality (1..100) grob auf PNG compress_level (0..9) abbilden: 100 → 0 (schnell), 1 → 9 (max. Kompression)
            compress_level = max(0, min(9, int(round((100 - quality) / 100 * 9))))
            img.save(out, format="PNG", compress_level=compress_level, optimize=False)
            filename = f"{base}.png"
            ctype = "image/png"
    except Exception:
        return HttpResponseBadRequest("Conversion failed.")

    out.seek(0)
    return FileResponse(out, as_attachment=True, filename=filename, content_type=ctype)
