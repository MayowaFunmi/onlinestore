import random
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def random_code(digit=7, letter=3):
    sample_str = ''.join((random.choice(string.digits) for i in range(digit)))
    sample_str += ''.join((random.choice(string.ascii_uppercase) for i in range(letter)))

    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string


class CustomUser(AbstractUser):
    code_number = models.CharField(default=random_code, max_length=10)


User = get_user_model()


# Create small form for admin user

class GetCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email_confirmed = models.BooleanField(default=False, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    photo = models.ImageField(upload_to='admin_pics/%Y/%m/%d/', null=True)
    id_card = models.FileField(upload_to='admin_docs/%Y/%m/%d/', null=True)
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    address = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    RELIGION = [
        ('Christian', 'Christianity'),
        ('Muslim', 'Islam'),
    ]
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.code_number})'


class ProductSeller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    address = models.CharField(max_length=300, null=True)
    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    RELIGION = [
        ('Christian', 'Christianity'),
        ('Muslim', 'Islam'),
    ]
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'


class ProductBuyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    address = models.CharField(max_length=300, null=True)
    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    RELIGION = [
        ('Christian', 'Christianity'),
        ('Muslim', 'Islam'),
    ]
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'


@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        GetCode.objects.create(user=instance)
        instance.getcode.save()


'''

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.getcode.save()

'''