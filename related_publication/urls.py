"""
related_publication/urls.py
──────────────────────────────────────────────────────────────────────────────
URL routing for the related_publication app.

Mount this file in the root urls.py with:
    path('related_publication/', include('related_publication.urls'))

Final resolved URL tree:
    GET  /related_publication/                              → publications_page (HTML render)
    GET  /related_publication/api/publications/             → api_get_publications
    POST /related_publication/api/publications/add/         → api_add_publication
    POST /related_publication/api/publications/update/      → api_update_publication
    POST /related_publication/api/publications/delete/      → api_delete_publication
"""

from django.urls import path
from . import views

app_name = "related_publication"

urlpatterns = [
    # ── Page renderer ─────────────────────────────────────────────────
    path(
        "",
        views.publications_page,
        name="page"
    ),

    # ── API: Read (GET) — all publications ────────────────────────────
    path(
        "api/publications/",
        views.api_get_publications,
        name="api_get"
    ),

    # ── API: Create (POST) ────────────────────────────────────────────
    path(
        "api/publications/add/",
        views.api_add_publication,
        name="api_add"
    ),

    # ── API: Update (POST / PUT) ──────────────────────────────────────
    path(
        "api/publications/update/",
        views.api_update_publication,
        name="api_update"
    ),

    # ── API: Delete (POST / DELETE) ───────────────────────────────────
    path(
        "api/publications/delete/",
        views.api_delete_publication,
        name="api_delete"
    ),
]
