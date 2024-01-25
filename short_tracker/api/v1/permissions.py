from rest_framework import permissions


class IsTeamLead(permissions.BasePermission):
    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.is_team_lead
