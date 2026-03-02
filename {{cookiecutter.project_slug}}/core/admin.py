from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import SiteSetting, Service, Product, TeamMember, ContactMessage


# ── Singleton admin for SiteSetting ──────────────────────────────────
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {
            "fields": ("site_name", "tagline"),
        }),
        ("Contact Information", {
            "fields": ("phone_primary", "phone_secondary", "email",
                       "address_line", "city", "state", "google_maps_embed_url"),
        }),
        ("Telegram Notifications", {
            "fields": ("telegram_bot_token", "telegram_chat_id"),
            "description": (
                "Enter your Telegram Bot token and Chat ID here to receive "
                "contact form submissions instantly. These override the "
                "TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID environment variables."
            ),
        }),
    )

    def has_add_permission(self, request):
        # Allow creation only if none exists yet
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect the list page straight to the single instance
        obj, _ = SiteSetting.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse("admin:core_sitesetting_change", args=[obj.pk])
        )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "received_at", "telegram_sent", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "telegram_sent")
    readonly_fields = ("name", "email", "phone", "subject", "message", "received_at", "telegram_sent")
    ordering = ("-received_at",)

    def has_add_permission(self, request):
        return False  # Only created via contact form
