from django.contrib import admin
from django.contrib.auth.models import User, Group

from .forms import DweetFormCK
from .models import Profile, Dweet


class DweetAdmin(admin.ModelAdmin):
    form = DweetFormCK
    list_display = ['user', 'created_at']
    # fieldsets = (
    #     (None, {
    #         "fields": (("user", "body"),)
    #     }),)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Dweet, DweetAdmin)
