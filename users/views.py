from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CustomUserCreationForm, LoginForm


# signup view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            context = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
            }
            return render(request, 'users/signup_success.html', context)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


# view for login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/shop/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# log out
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/shop/')
