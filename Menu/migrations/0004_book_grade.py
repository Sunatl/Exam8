# Generated by Django 5.0 on 2024-12-05 06:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0003_remove_payment_wallet_customuser_is_actives'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Menu.grade'),
        ),
    ]
