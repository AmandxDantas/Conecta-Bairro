import json
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def route_manifest(_request):
    """Responde ao manifesto como JSON bruto, sem o fallback de uma aplicação."""
    manifest = Path(settings.BASE_DIR) / "manus-routes.json"
    return HttpResponse(manifest.read_text(encoding="utf-8"), content_type="application/json")


urlpatterns = [
    path("manus-routes.json", route_manifest, name="manus_routes"),
    path("admin/", admin.site.urls),
    path("conta/", include("accounts.urls")),
    path("", include("professionals.urls")),
]
