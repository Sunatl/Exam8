# Generated by Django 5.0 on 2024-12-04 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Menu.wallet'),
        ),
    ]