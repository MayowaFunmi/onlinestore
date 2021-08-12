from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, GetCode, ProductBuyer, ProductSeller

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'code_number', 'email', 'first_name', 'last_name']
    # list_filter = ['status']
    # search_fields = ('status',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GetCode)
admin.site.register(ProductBuyer)
admin.site.register(ProductSeller)