from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields to the user profile as needed

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class FeedbackLink(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    link = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)  # Add a name field
    description = models.TextField()  # Add a description field

class Feedback(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    feedbacklink = models.ForeignKey(FeedbackLink, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
