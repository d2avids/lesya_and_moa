from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        'id',
        'email',
    )
    search_fields = (
        'email',
    )

    filter_horizontal = ()
    fieldsets = ()
