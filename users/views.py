from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Your account has been created! You are now logged in.')
            return redirect('home')  # Replace 'home' with the URL where you want to redirect after registration
        else:
            messages.warning(request, 'Unable to create an account. Please correct the errors below.')
    else:
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Profile Registration'})

@login_required
def profile(request):
    user = request.user
    profile = user.profile
    context = {'user': user, 'profile': profile}
    return render(request, 'profile.html', context)
