# Generated by Django 4.2.1 on 2023-07-23 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prodect_name',
            new_name='product_name',
        ),
    ]
