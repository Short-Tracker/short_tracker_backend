from rest_framework import permissions


class IsTeamLead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_team_lead


class isLeadOrPerformerHimselfOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        is_lead = request.user.is_lead
        return request.user.id == request.data.get('performers')[0] or is_lead
