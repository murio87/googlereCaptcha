from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .decorators import user_not_authenticated


@user_not_authenticated
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been cretaed successfully')
            return redirect('login')
        else:
            for error in list(form.errors):
                print(request, error)
    else:
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are logout')
    return redirect('home')


@user_not_authenticated
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in successfully')
                return redirect('home')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, 'You must pass the reCAPTCHA test')
                    continue
                messages.error(request, error)

    form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def profile_view(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated')
            return redirect('profile', user_form.username)

        for error in list(form.errors):
            print(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserProfileUpdateForm(instance=user)
        return render(request, 'users/profile.html', {'form': form})
    return redirect('home')
