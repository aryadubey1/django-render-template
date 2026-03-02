import requests
from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import SiteSetting, Service, Product, TeamMember, ContactMessage


# ─────────────────────────────────────────────
# Telegram helper
# ─────────────────────────────────────────────

def _send_telegram(bot_token: str, chat_id: str, text: str) -> bool:
    """Send a message via Telegram Bot API. Returns True on success."""
    if not bot_token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=8)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def _get_telegram_credentials(site_config: SiteSetting):
    """
    Returns (bot_token, chat_id).
    Admin panel values take priority; falls back to .env values.
    """
    token = (
        site_config.telegram_bot_token.strip()
        if site_config and site_config.telegram_bot_token
        else ""
    ) or getattr(django_settings, "TELEGRAM_BOT_TOKEN", "")

    chat_id = (
        site_config.telegram_chat_id.strip()
        if site_config and site_config.telegram_chat_id
        else ""
    ) or getattr(django_settings, "TELEGRAM_CHAT_ID", "")

    return token, chat_id


# ─────────────────────────────────────────────
# Context helper — injects site settings into all views
# ─────────────────────────────────────────────

def _base_context():
    return {"settings": SiteSetting.load()}


# ─────────────────────────────────────────────
# Views
# ─────────────────────────────────────────────

def home(request):
    ctx = _base_context()
    # ctx['featured_services'] = Service.objects.filter(is_active=True)[:3]
    # ctx['featured_products'] = Product.objects.filter(is_active=True, is_featured=True)[:3]
    return render(request, 'core/home.html', ctx)


def about(request):
    ctx = _base_context()
    # ctx['team_members'] = TeamMember.objects.all()
    return render(request, 'core/about.html', ctx)


def services(request):
    ctx = _base_context()
    # ctx['services'] = Service.objects.filter(is_active=True)
    return render(request, 'core/services.html', ctx)


def products(request):
    ctx = _base_context()
    # ctx['products'] = Product.objects.filter(is_active=True)
    return render(request, 'core/products.html', ctx)


def contact(request):
    site_config = SiteSetting.load()
    ctx = {"settings": site_config}

    if request.method == "POST":
        name    = request.POST.get("name",    "").strip()
        email   = request.POST.get("email",   "").strip()
        phone   = request.POST.get("phone",   "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not all([name, email, subject, message]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'core/contact.html', ctx)

        # ── Save to database ──
        contact_msg = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        # ── Send via Telegram ──
        bot_token, chat_id = _get_telegram_credentials(site_config)
        if bot_token and chat_id:
            telegram_text = (
                f"📩 <b>New Contact Message</b>\n\n"
                f"👤 <b>Name:</b> {name}\n"
                f"📧 <b>Email:</b> {email}\n"
                f"📱 <b>Phone:</b> {phone or 'Not provided'}\n"
                f"📌 <b>Subject:</b> {subject}\n\n"
                f"💬 <b>Message:</b>\n{message}"
            )
            sent = _send_telegram(bot_token, chat_id, telegram_text)
            contact_msg.telegram_sent = sent
            contact_msg.save(update_fields=["telegram_sent"])

            if not sent:
                # Log but don't fail the user experience
                import logging
                logging.getLogger(__name__).warning(
                    "Telegram notification failed for ContactMessage pk=%s", contact_msg.pk
                )

        messages.success(
            request,
            f"Thanks {name}! Your message has been received. We'll get back to you shortly."
        )
        return redirect("contact")

    return render(request, 'core/contact.html', ctx)
