from django.contrib import admin

from api.models import User, Project, Contributor, Issue, Comment


class UserAdmin(admin.ModelAdmin):

    list_display = ["email", "first_name", "last_name", "id"]


class ProjectAdmin(admin.ModelAdmin):

    list_display = ["title", "author", "id"]
    list_filter = ["author"]


class ContributorAdmin(admin.ModelAdmin):

    list_filter = ["user", "project"]


class IssueAdmin(admin.ModelAdmin):

    list_display = ["title", "status", "author", "user_in_charge", "id"]
    list_filter = ["author"]


class CommentAdmin(admin.ModelAdmin):

    list_display = ["description", "issue", "author", "id"]
    list_filter = ["author", "issue"]


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
