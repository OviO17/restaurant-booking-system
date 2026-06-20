from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookings"

    def ready(self):
        """Register profile lifecycle signals when Django starts."""
        from . import signals  # noqa: F401
