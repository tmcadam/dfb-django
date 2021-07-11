# Generated by Django 3.2.5 on 2021-07-11 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biographies', '0004_alter_biography_primary_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='authors',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='external_links',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='references',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='revisions',
            field=models.TextField(null=True),
        ),
    ]
