# Generated by Django 4.2.4 on 2024-11-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maricho', '0007_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.TextField(default='Enter the title'),
        ),
    ]