# Generated by Django 4.2.3 on 2023-09-09 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_offer'),
        ('category', '0009_brand_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='admincategory',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.offer'),
        ),
    ]