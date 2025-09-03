from django.urls import path
from django.views.generic import TemplateView
from . import views
from .forms import ImageUploadForm  # dein bestehendes Form

app_name = "weconvert"

urlpatterns = [
    # GET: Seite rendern (ohne convert_view)
    path(
        "",
        TemplateView.as_view(
            template_name="weconvert/upload.html",
            extra_context={"form": ImageUploadForm()},
        ),
        name="page",
    ),

    # POST: eigentliche Konvertierung (deine Funktion von vorhin)
    path("run/", views.convert_to_png, name="convert"),
]