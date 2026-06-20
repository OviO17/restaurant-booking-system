from django.db import migrations, models
from django.db.models import Q


def create_missing_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Client = apps.get_model("bookings", "Client")
    linked_user_ids = Client.objects.exclude(user_id=None).values_list(
        "user_id",
        flat=True,
    )

    for user in User.objects.exclude(id__in=linked_user_ids):
        email = user.email or f"{user.username}@users.local"
        if Client.objects.filter(email=email).exists():
            email = f"{user.username}-{user.pk}@users.local"
        Client.objects.create(
            user=user,
            full_name=user.get_full_name() or user.username,
            email=email,
            phone="",
        )


class Migration(migrations.Migration):
    dependencies = [("bookings", "0003_client_user")]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.RemoveConstraint(
            model_name="reservation",
            name="unique_table_booking_per_slot",
        ),
        migrations.AddConstraint(
            model_name="reservation",
            constraint=models.UniqueConstraint(
                condition=Q(status="confirmed"),
                fields=("table", "date", "time"),
                name="unique_confirmed_table_booking_per_slot",
            ),
        ),
        migrations.RunPython(create_missing_profiles, migrations.RunPython.noop),
    ]
