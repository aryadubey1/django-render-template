from django.db import models


class SiteSetting(models.Model):
    """
    Global site settings — editable in admin.
    Telegram tokens here override the .env values.
    Only one row should ever exist (enforced in admin).
    """
    site_name = models.CharField(max_length=150, default="{{cookiecutter.project_name}}")
    tagline = models.CharField(
        max_length=200,
        default="{{cookiecutter.description}}",
    )
    phone_primary = models.CharField(max_length=30, blank=True)
    phone_secondary = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address_line = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    google_maps_embed_url = models.URLField(
        blank=True,
        max_length=1000,
        help_text="Paste the full Google Maps embed URL for the Contact page map.",
    )
    telegram_bot_token = models.CharField(
        max_length=255,
        blank=True,
        help_text="Bot token used to send Contact messages to Telegram. Overrides TELEGRAM_BOT_TOKEN env var.",
    )
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Chat ID / channel ID that receives Contact messages. Overrides TELEGRAM_CHAT_ID env var.",
    )

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Global Site Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton — always pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(
        max_length=100, default='fa-star',
        help_text="FontAwesome class e.g. fa-gear, fa-bolt"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100, default='all')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    telegram_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"
