# Generated by Django 5.0 on 2024-12-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0002_payment_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='wallet',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_actives',
            field=models.BooleanField(default=False),
        ),
    ]
