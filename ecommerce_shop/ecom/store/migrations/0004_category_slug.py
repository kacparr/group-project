# Generated by Django 5.1.5 on 2025-02-03 09:35

from django.db import migrations
from django.utils.text import slugify 


def populate_slug(apps, schema_editor):
    Category = apps.get_model('store','Category')
    for cat in Category.objects.all():
        cat.slug = slugify(cat.name)
        cat.save()
class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_product_products'),
    ]

    operations = [
        migrations.RunPython(populate_slug),
    ]
