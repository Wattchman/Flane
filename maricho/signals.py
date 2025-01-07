#  this file is for signals
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserActivity, AdImpression
from django.contrib.auth.signals import user_logged_in, user_logged_out

@receiver(post_save, sender=UserActivity)
def track_activity(sender, instance, created, **kwargs):
    if created:
        post_save.disconnect(track_activity, sender=UserActivity)

        if instance.activity_type not in ['login', 'logout']:

            UserActivity.objects.create(
            user=instance.user,
            activity_type=instance.activity_type,
            additional_data=instance.additional_data,
            activity_time=instance.activity_time
        )
            post_save.connect(track_activity, sender=UserActivity)

@receiver(user_logged_in)
def track_login(sender, user, request, **kwargs):
    UserActivity.objects.create(user=user, activity_type='login', activity_time=timezone.now())

@receiver(user_logged_out)
def track_logout(sender, user, request, **kwargs):
    UserActivity.objects.create(user=user, activity_type='logout', activity_time=timezone.now())

