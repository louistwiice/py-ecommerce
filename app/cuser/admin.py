from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_active', 'has_picture', 'phone_number']
    search_fields = ['username', 'first_name', 'last_name', 'phone_number']

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

    def has_picture(self, obj) -> bool:
        if obj.picture:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')

        return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')


admin.site.register(User, CustomUserAdmin)
