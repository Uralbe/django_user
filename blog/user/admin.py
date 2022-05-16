from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user import models

admin.site.site_title = 'Dona uz'
admin.site.site_header = 'Dona uz'
admin.site.site_url = 'https://dona.uz/'

admin.site.index_title = 'Bosh sahifa'


admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ['firstname', 'lastname',
                    'phone_number']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password',
                           'firstname', 'lastname')}),
        # (_('Personal Info'),{'fields': ('id', )}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser',)
            }
        ),
        (_('Important Dates'), {
            'fields': ('last_login', )
        }),
    )
    add_fieldsets = (
        (None, {'classes': ('wide'),
                'fields': ('firstname',
                           'lastname',
                           'phone_number',
                           'password1',
                           'password2')
                }),
    )
    search_fields = ('phone_number', 'firstname', 'lastname')
    ordering = ('phone_number',)


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['contact', 'code']
    search_fields = ['contact']
