# Generated by Django 4.2.16 on 2024-12-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0002_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]
