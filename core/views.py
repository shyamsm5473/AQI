"""
core/views.py  —  Page render views + authentication for the IIIT Lucknow portal.
Each view renders its Django template and passes an active_page context
variable so the shared base.html navbar highlights the correct link.

Authentication uses Django's built-in django.contrib.auth system:
  - login_view         : GET renders form / POST authenticates and redirects
  - signup_view        : GET renders form / POST creates User and auto-logs in
  - logout_view        : POST clears the session
  - forgot_password_view : GET shows email form / POST sends OTP to registered email
  - verify_otp_view    : GET shows OTP form / POST validates OTP and redirects to reset
  - reset_password_view: GET shows new-password form / POST sets new password
"""
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetOTP


def home(request):
    return render(request, "core/home.html", {"active_page": "home"})

def about(request):
    return render(request, "core/about.html", {"active_page": "about"})

def dashboard(request):
    return render(request, "core/dashboard.html", {"active_page": "dashboard"})

def analytics(request):
    return render(request, "core/analytics.html", {"active_page": "analytics"})

@ensure_csrf_cookie
def contact(request):
    return render(request, "core/contact.html", {"active_page": "contact"})

def benefits(request):
    return render(request, "core/benefits.html", {"active_page": "benefits"})

def map_view(request):
    return render(request, "core/map.html", {"active_page": "map"})


# ── Authentication Views ───────────────────────────────────────────────────────

@csrf_protect
def login_view(request):
    """
    GET  → render the login page.
    POST → authenticate credentials; on success redirect to next param or home.
    """
    # Already logged-in users go straight to home
    if request.user.is_authenticated:
        return redirect('core:home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            error = 'Both username and password are required.'
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Honor ?next= redirect param (e.g. after @login_required)
                next_url = request.GET.get('next') or request.POST.get('next', '')
                return redirect(next_url if next_url else 'core:home')
            else:
                error = 'Invalid username or password. Please try again.'

    return render(request, 'core/login.html', {
        'active_page': 'login',
        'error': error,
        'next': request.GET.get('next', ''),
    })


@csrf_protect
def signup_view(request):
    """
    GET  → render the signup / registration page.
    POST → validate fields, create a new User, auto-login, redirect to home.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    error = None
    form_data = {}  # Preserve filled values on validation failure

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name',  '').strip()
        username   = request.POST.get('username',   '').strip()
        email      = request.POST.get('email',      '').strip()
        password1  = request.POST.get('password1',  '')
        password2  = request.POST.get('password2',  '')

        form_data = {
            'first_name': first_name, 'last_name': last_name,
            'username': username, 'email': email,
        }

        # ── Validation chain ───────────────────────────────────────────
        if not all([first_name, username, email, password1, password2]):
            error = 'All fields marked * are required.'
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif len(password1) < 8:
            error = 'Password must be at least 8 characters long.'
        elif User.objects.filter(username=username).exists():
            error = f'Username "{username}" is already taken. Please choose another.'
        elif User.objects.filter(email=email).exists():
            error = 'An account with this email address already exists.'
        else:
            # ── Create the user and auto-login ─────────────────────────
            user = User.objects.create_user(
                username   = username,
                email      = email,
                password   = password1,
                first_name = first_name,
                last_name  = last_name,
            )
            login(request, user)
            return redirect('core:home')

    return render(request, 'core/signup.html', {
        'active_page': 'signup',
        'error': error,
        'form_data': form_data,
    })


@require_http_methods(["POST"])
def logout_view(request):
    """
    POST → log out the current user and redirect to home.
    We use POST (not GET) to protect against CSRF logout attacks.
    """
    logout(request)
    return redirect('core:home')


# ── Contact form POST API ──────────────────────────────────────────────────────

@csrf_protect
@require_http_methods(["POST"])
def contact_submit(request):
    """
    Receives the contact form JSON payload from the fetch() call in contact.html.
    Logs submission to console. Replace print() with Django send_mail() or a
    ContactMessage model to persist / email submissions in production.
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid JSON payload."}, status=400)

    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return JsonResponse({"success": False, "error": "All fields are required."}, status=400)

    print(f"\n[CONTACT FORM]\nFrom : {name} <{email}>\nMsg  : {message}\n")

    return JsonResponse({"success": True, "message": f"Thanks, {name}! We received your message."})


# ── Password Reset (OTP via Email) ─────────────────────────────────────────────

@csrf_protect
def forgot_password_view(request):
    """
    GET  → show email input form.
    POST → look up user by email, generate OTP, send it, redirect to verify page.
    """
    error = None
    success = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        if not email:
            error = 'Please enter your registered email address.'
        else:
            try:
                user = User.objects.get(email__iexact=email)
                otp_obj = PasswordResetOTP.generate_for(user)

                # Send OTP email
                subject = 'IIIT Lucknow — Your Password Reset OTP'
                body = (
                    f"Hi {user.first_name or user.username},\n\n"
                    f"Your one-time password (OTP) for resetting your IIIT Lucknow account password is:\n\n"
                    f"        {otp_obj.otp}\n\n"
                    f"This OTP is valid for 10 minutes. Do not share it with anyone.\n\n"
                    f"If you did not request a password reset, please ignore this email.\n\n"
                    f"— IIIT Lucknow Team"
                )
                try:
                    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
                    # Store user id in session so verify page knows who to reset
                    request.session['otp_user_id'] = user.id
                    return redirect('core:verify_otp')
                except Exception as e:
                    error = 'Could not send email. Please check your email configuration or try again later.'
                    print(f"[EMAIL ERROR] {e}")

            except User.DoesNotExist:
                # Don't reveal whether email exists — show generic message
                error = 'If this email is registered, an OTP has been sent to it.'

    return render(request, 'core/forgot_password.html', {
        'active_page': 'forgot_password',
        'error': error,
        'success': success,
    })


@csrf_protect
def verify_otp_view(request):
    """
    GET  → show OTP entry form.
    POST → validate OTP; on success redirect to reset-password page.
    """
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('core:forgot_password')

    error = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()

        try:
            user = User.objects.get(pk=user_id)
            otp_obj = PasswordResetOTP.objects.filter(
                user=user, otp=entered_otp, is_used=False
            ).order_by('-created_at').first()

            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                # Mark session as OTP-verified so reset page allows access
                request.session['otp_verified_user_id'] = user.id
                del request.session['otp_user_id']
                return redirect('core:reset_password')
            else:
                error = 'Invalid or expired OTP. Please try again or request a new one.'

        except User.DoesNotExist:
            return redirect('core:forgot_password')

    return render(request, 'core/verify_otp.html', {
        'active_page': 'verify_otp',
        'error': error,
    })


@csrf_protect
def reset_password_view(request):
    """
    GET  → show new-password form.
    POST → set new password, clear session, redirect to login.
    """
    user_id = request.session.get('otp_verified_user_id')
    if not user_id:
        return redirect('core:forgot_password')

    error = None

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            error = 'Both password fields are required.'
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif len(password1) < 8:
            error = 'Password must be at least 8 characters long.'
        else:
            try:
                user = User.objects.get(pk=user_id)
                user.set_password(password1)
                user.save()
                del request.session['otp_verified_user_id']
                return render(request, 'core/reset_password.html', {
                    'active_page': 'reset_password',
                    'success': True,
                })
            except User.DoesNotExist:
                return redirect('core:forgot_password')

    return render(request, 'core/reset_password.html', {
        'active_page': 'reset_password',
        'error': error,
        'success': False,
    })
