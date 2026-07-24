"""
iiitl_project/urls.py  —  Root URL configuration
"""
from django.contrib             import admin
from django.urls                import path, include
from django.conf                import settings
from django.conf.urls.static   import static
from django.views.generic       import TemplateView  # For Google Search Console verification

urlpatterns = [
    path("admin/", admin.site.urls),

    # ── Google Search Console ownership verification ───────────────────────────
    # Place google84ea73e41abe6313.html inside BASE_DIR/templates/
    path(
        "google84ea73e41abe6313.html",
        TemplateView.as_view(
            template_name="google84ea73e41abe6313.html",
            content_type="text/html",
        ),
        name="google-search-console-verify",
    ),

    # Core site pages (home, about, dashboard, analytics, contact, benefits, map)
    path("", include("core.urls")),

    # Publications app
    path("related_publication/", include("related_publication.urls")),

] + static(settings.STATIC_URL, document_root=settings.BASE_DIR)
