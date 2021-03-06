# Generated by Django 3.1.7 on 2021-04-05 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_auto_20210405_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='service_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='useraccount.services'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
