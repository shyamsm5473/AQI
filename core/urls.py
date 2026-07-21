"""
core/urls.py  —  URL routes for all site pages served by the core app.
"""
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("",          views.home,           name="home"),
    path("about/",    views.about,          name="about"),
    path("dashboard/",views.dashboard,      name="dashboard"),
    path("analytics/",views.analytics,      name="analytics"),
    path("contact/",  views.contact,        name="contact"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("benefits/", views.benefits,       name="benefits"),
    path("map/",      views.map_view,       name="map"),
    # ── Authentication ─────────────────────────────────────
    path("login/",    views.login_view,     name="login"),
    path("signup/",   views.signup_view,    name="signup"),
    path("logout/",   views.logout_view,    name="logout"),
    # ── Password Reset (OTP) ───────────────────────────────
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("verify-otp/",      views.verify_otp_view,      name="verify_otp"),
    path("reset-password/",  views.reset_password_view,  name="reset_password"),
]
