from django.contrib import admin

from api.models import User, Project, Contributor


class UserAdmin(admin.ModelAdmin):

    list_display = ["email", "first_name", "last_name"]


class ProjectAdmin(admin.ModelAdmin):

    list_display = ["title", "author"]


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor)
