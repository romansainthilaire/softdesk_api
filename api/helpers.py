from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied

from api.models import Project, Contributor, Issue, Comment


def check_project_contributor_access(project_id, user):
    project = get_object_or_404(Project, pk=project_id)
    user_contributors = Contributor.objects.filter(user=user)
    if len(Project.objects.filter(pk=project.pk, contributors__in=user_contributors)) == 0:
        raise PermissionDenied("Accès refusé. Vous n'êtes pas un contributeur de ce projet.")


def check_project_author_access(project_id, user):
    project = get_object_or_404(Project, pk=project_id)
    if user != project.author:
        raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce projet.")


def check_issue_author_access(issue_id, user):
    issue = get_object_or_404(Issue, pk=issue_id)
    if user != issue.author:
        raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce problème.")


def check_comment_author_access(comment_id, user):
    comment = get_object_or_404(Comment, pk=comment_id)
    if user != comment.author:
        raise PermissionDenied("Opération annulée. Vous n'êtes pas l'auteur de ce commentaire.")
