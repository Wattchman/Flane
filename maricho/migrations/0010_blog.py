# Generated by Django 4.2.4 on 2024-03-13 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maricho', '0009_profile_id_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to='blog_images')),
                ('Body', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
