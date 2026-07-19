"""
iiitl_project/urls.py  —  Root URL configuration
"""
from django.contrib import admin
from django.urls    import path, include
from django.conf    import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core site pages (home, about, dashboard, analytics, contact, benefits, map)
    path("", include("core.urls")),

    # Publications app
    path("related_publication/", include("related_publication.urls")),

] + static(settings.STATIC_URL, document_root=settings.BASE_DIR)
