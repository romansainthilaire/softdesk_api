from django.contrib import admin

from api.models import User, Project


class UserAdmin(admin.ModelAdmin):

    list_display = ["username", "first_name", "last_name", "email", "id"]


class ProjectAdmin(admin.ModelAdmin):

    list_display = ["title", "author"]


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
