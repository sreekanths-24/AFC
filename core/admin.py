from django.contrib import admin
from .models import UserProfile, Feedback, FeedbackLink

# Register your models here
admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(FeedbackLink)
