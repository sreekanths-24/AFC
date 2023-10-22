from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's built-in views for authentication

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('create_feedback_link/', views.create_feedback_link, name='create_feedback_link'),
    path('submit_feedback/<str:link>/', views.submit_feedback, name='submit_feedback'),
    path('custom_logout/', views.custom_logout, name='custom_logout'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('delete_feedback_link/<uuid:link>/', views.delete_feedback_link, name='delete_feedback_link'),
]
