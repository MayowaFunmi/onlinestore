from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from .forms import CustomUserCreationForm, LoginForm, GetCodeForm, AdminSignUpForm, AdminLoginForm
from django.views import generic
from .models import GetCode
from .tokens import account_activation_token


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
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MyShop Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            recipient = form.cleaned_data['email']
            #user.email_user(subject, message)
            send_mail(subject, message, 'mayordecoder@gmail.com', [recipient])
            messages.success(request, 'Please Confirm your email to complete registration.')
            return render(request, 'users/account_activation_sent.html')

        return render(request, self.template_name, {'form': form})

'''
# function based view for admin signup

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MyShop Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, "Account Confirmaton Link Sent To Your Email")
            return render(request, 'users/account_activation_sent.html')
        else:
            messages.error(request, "Failed To Send Account Confirmaton Link To Your Email")
            return render(request, 'users/account_activation_invalid.html')

    else:
        form = AdminSignUpForm()
    return render(request, 'users/admin_signup.html', {'form': form})
'''


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')

# activate admin

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_staff = True
            user.getcode.email_confirmed = True
            user.save()
            login(request, user)
            return render(request, 'users/activate_email_success.html')
        else:
            return render(request, 'users/account_activation_invalid.html')


#views for admin get code

@login_required
@transaction.atomic
def get_code(request):
    if request.method == 'POST':
        form = GetCodeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
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

            # send to owner's email
            print(request.user)
            print(profile)
            subject = f'Code for {request.user.first_name} {request.user.last_name}'
            message = f'Hi {request.user.first_name}, Thank you for your interest' \
                    f'Below is your login code to be one of our administrators' \
                    f'{request.user.code_number}'
            email_from = 'mayordecoder@gmail.com'
            recipient = request.user.email

            send_mail(subject, message, email_from, [recipient], fail_silently=False)
            return render(request, 'users/your_code.html')
    else:
        form = GetCodeForm()

    return render(request, 'users/get_admin_code.html', {'form': form})


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
        form = LoginForm()
    return render(request, 'users/admin_login.html', {'form': form})



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


'''
    phone_number = forms.CharField(label='Phone Number', max_length=20, widget=forms.TextInput())
    photo = forms.FileField(label='Profile Picture', widget=forms.FileInput())
    id_card = forms.ImageField(label='ID Card', widget=forms.FileInput())
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER, widget=forms.Select())
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput())
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput())
    RELIGION = [
        ('Christian', 'Christianity'),
        ('Muslim', 'Islam'),
    ]
    religion = forms.ChoiceField(label='Religion', choices=RELIGION, widget=forms.Select())
    about_me = forms.CharField(label="About me", max_length=50, widget=forms.Textarea())
'''