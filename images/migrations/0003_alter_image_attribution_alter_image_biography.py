# Generated by Django 4.2.3 on 2024-10-01 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biographies', '0010_alter_biographyauthor_unique_together_and_more'),
        ('images', '0002_add_images_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='attribution',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='biography',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='biographies.biography'),
        ),
    ]
