# Generated by Django 5.1.5 on 2025-02-03 09:45

from django.db import migrations
from django.utils.text import slugify

def populate_slug(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    for category in Category.objects.all():
        category.slug = slugify(category.name)
        category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slug),
    ]
