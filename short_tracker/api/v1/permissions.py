from rest_framework import permissions


class IsTeamLead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_team_lead


class IsLeadOrPerformerHimselfOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        is_lead = request.user.is_authenticated and request.user.is_team_lead
        return is_lead or (
            request.user.is_authenticated
            and request.user.id == request.data.get('performers')[0]
        )


class IsCreatorOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        is_lead = request.user.is_authenticated and request.user.is_team_lead
        return is_lead or (
            request.user.is_authenticated
            and request.user.id == request.data.get('performers')[0]
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.id == obj.creator.id)
