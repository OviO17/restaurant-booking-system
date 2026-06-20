from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client


def profile_defaults(user):
    """Return safe profile values for users created outside the signup page."""
    return {
        "full_name": user.get_full_name() or user.username,
        "email": user.email or f"{user.username}@users.local",
        "phone": "",
    }


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """Ensure admin-created users and superusers also receive a Client profile."""
    if created:
        defaults = profile_defaults(instance)
        existing = Client.objects.filter(
            email=defaults["email"],
            user__isnull=True,
        ).first()
        if existing:
            existing.user = instance
            existing.save(update_fields=["user"])
        else:
            if Client.objects.filter(email=defaults["email"]).exists():
                defaults["email"] = f"{instance.username}-{instance.pk}@users.local"
            Client.objects.get_or_create(user=instance, defaults=defaults)
