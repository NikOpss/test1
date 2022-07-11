from django.contrib import admin
from .models import NewUser, UserBalance
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea




class UserAdminConfig(UserAdmin):

    search_fields = ('email', 'username', 'first_name')
    list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields':('email', 'username', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )

    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols':40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


# class UserBalanceConfig(UserAdmin):
#     search_fields = ('user', 'balance')
#     list_filter = ('user', 'balance')
#     list_display = ('user', 'balance')




admin.site.register(NewUser, UserAdminConfig)
admin.site.register(UserBalance)


# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('name', 'balance')
# admin.site.register(Bank, CustomerAdmin )