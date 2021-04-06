# Generated by Django 3.1.7 on 2021-04-06 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0005_auto_20210405_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='service_id',
        ),
        migrations.AddField(
            model_name='services',
            name='service_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='useraccount.category'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
