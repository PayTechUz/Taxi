from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import UserChangeForm, UserCreationForm

from apps.authentication.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'display_role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    list_filter_submit = True
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

    @display(
        description=_("Role"),
        label={
            "admin": "danger",
            "driver": "success",
            "client": "info",
        },
    )
    def display_role(self, obj):
        return obj.role


from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)
