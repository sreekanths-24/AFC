from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Feedback, FeedbackLink
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.auth import logout

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profile')  # Redirect to the user's profile page
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to your login page
# User Profile View (Requires login)
@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    feedback_links = FeedbackLink.objects.filter(user=user_profile)
    
    # Create a list of dictionaries for each feedback link with associated feedbacks
    feedbacks_data = []
    for link in feedback_links:
        feedbacks = Feedback.objects.filter(feedbacklink=link)
        feedbacks_data.append({'link': link, 'feedbacks': feedbacks})

    return render(request, 'core/user_profile.html', {'user_profile': user_profile, 'feedbacks_data': feedbacks_data})
@login_required
def create_feedback_link(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        name = request.POST.get('name')  # Get the name from the form
        description = request.POST.get('description')  # Get the description from the form

        # Create a new feedback link with the provided name and description
        feedback_link = FeedbackLink(user=user_profile, link=str(uuid.uuid4()), name=name, description=description)
        feedback_link.save()
        
        return redirect('profile')  # Redirect to the user's profile page

    return render(request, 'core/create_feedback_link.html')

# Submit Feedback View
def submit_feedback(request, link):
    try:
        feedback_link = FeedbackLink.objects.get(link=link)
    except FeedbackLink.DoesNotExist:
        # Handle case where the link doesn't exist
        return render(request, 'core/invalid_link.html')

    if request.method == 'POST':
        text = request.POST['text']
        user_profile = UserProfile.objects.get(user=feedback_link.user.user)
        feedback = Feedback(text=text, user=user_profile, feedbacklink=feedback_link)
        feedback.save()
        return redirect('thank_you')  # Redirect to a "thank you" page
    return render(request, 'core/submit_feedback.html', {'feedback_link': feedback_link})

def thank_you(request):
    return render(request, 'core/thank_you.html')

from django.http import JsonResponse

# ... Other views

@login_required
def delete_feedback_link(request, link):
    try:
        feedback_link = FeedbackLink.objects.get(link=link, user=request.user.userprofile)
        feedback_link.delete()
        return JsonResponse({'success': True})
    except FeedbackLink.DoesNotExist:
        return JsonResponse({'success': False})