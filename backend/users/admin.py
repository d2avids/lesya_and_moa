from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework.authtoken.models import TokenProxy
from django.contrib.auth.models import Group
from django.conf import settings

from users.models import ChildrenGroup, User, Region, Child


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    from django.utils.translation import gettext_lazy as _

    fieldsets = (
        (
            None,
            {"fields": ("password", "tasks_type", "data_processing_agreement")}
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "password1", "password2", "email"),
            },
        ),
    )
    list_display = (
        "id", "email", "first_name", "last_name", "tasks_type", "is_staff"
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    search_fields = (
        'name',
    )
    ordering = ('name',)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'sex',
        'age',
        'region',
        'attended_speech_therapist',
        'user',
        'parent_id',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'sex',
        'attended_speech_therapist',
    )
    ordering = ('id',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('region', 'user')

    @admin.display(description='id родителя/логопеда')
    def parent_id(self, obj):
        return obj.user.id


@admin.register(ChildrenGroup)
class ChildrenGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'number_of_students',
        'region',
        'user',
    )
    search_fields = (
        'name',
    )
    ordering = ('id',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('region', 'user')

    @admin.display(description='id педагога')
    def educator_id(self, obj):
        return obj.user.id


admin.site.unregister(Group)
if not settings.DEBUG:
    admin.site.unregister(TokenProxy)
