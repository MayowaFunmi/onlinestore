from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import CustomUserCreationForm, LoginForm, GetCodeForm, AdminSignUpForm, AdminLoginForm
from django.views import generic
from .models import GetCode


User = get_user_model()

# class based view for admin signup

class AdminSignUpView(View):
    form_class = AdminSignUpForm
    template_name = 'users/admin_signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return render(request, 'users/signup_success.html')

        return render(request, self.template_name, {'form': form})


# admin login
def admin_user_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'], unique_id=cd['registration_number'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'users/admin_welcome.html')
    else:
        form = AdminLoginForm()
    return render(request, 'users/admin_login.html', {'form': form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        form = GetCodeForm(instance=request.user.getcode, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=True)

            photo = request.FILES['photo']
            fs = FileSystemStorage()
            photo_filename = fs.save(photo.name, photo)

            id_card = request.FILES['id_card']
            fs = FileSystemStorage()
            card_filename = fs.save(id_card.name, id_card)

            context = {
                'user': request.user,
                'code_number': request.user.code_number,
                'phone_number': form.cleaned_data['phone_number'],
                'email': request.user.email,
                'gender': form.cleaned_data['gender'],
                'address': form.cleaned_data['address'],
                'date_of_birth': form.cleaned_data['date_of_birth'],
                'religion': form.cleaned_data['religion'],
                'about_me': form.cleaned_data['about_me'],
                'photo_url': fs.url(photo_filename),
                'id_card_url': fs.url(card_filename),
            }
            return render(request, 'users/admin_profile_details.html', context)
        else:
            print(form.errors)
            print("Invalid Form")
    else:
        form = GetCodeForm()
    return render(request, 'users/get_admin_code.html', {'form': form})


class AdminRegister(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:signup_success')
    template_name = 'users/register.html'


def SignUpSuccess(request):
    return render(request, 'users/signup_success.html')

# login

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'users/welcome.html')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/shop/')


'''
            try:
                phone_number = form.cleaned_data['phone_number']
                gender = form.cleaned_data['gender']
                address = form.cleaned_data['address']
                date_of_birth = form.cleaned_data['date_of_birth']
                religion = form.cleaned_data['religion']
                about_me = form.cleaned_data['about_me']

                photo = request.FILES['photo']
                fs = FileSystemStorage()
                photo_filename = fs.save(photo.name, photo)
                photo_url = fs.url(photo_filename)

                id_card = request.FILES['id_card']
                fs = FileSystemStorage()
                card_filename = fs.save(id_card.name, id_card)
                id_card_url = fs.url(card_filename)
                print(id_card_url)

                profile = GetCode.objects.get(user=request.user)
                profile.email_confirmed = True
                profile.phone_number = phone_number
                profile.photo = photo_url
                profile.id_card = id_card_url
                profile.gender = gender
                profile.address = address
                profile.date_of_birth = date_of_birth
                profile.religion = religion
                profile.about_me = about_me
                profile.save()

                print(request.user)
                print(profile)
                return render(request, 'users/your_code.html')

            except:
                return render(request, 'users/get_admin_code.html',)
'''