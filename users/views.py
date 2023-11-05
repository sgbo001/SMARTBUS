from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileEditForm, UserRegisterForm, UserProfileForm
from .models import Profile

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

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('route_plan')

    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})