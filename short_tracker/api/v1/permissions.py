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


class IsCreatorAndLidOrPerformerOnly(permissions.BasePermission):
    """
    Задачу может менять создатель задачи и Лидер.
    Исполнитель может менять только статус задачи.
    """
    def has_object_permission(self, request, view, obj):

        is_lead = request.user.is_team_lead
        perf = []
        for performer in obj.performers.values():
            perf.append(performer.get('id'))
        a = (request.user.id in perf and len(request.data) == 1
             and 'status' in request.data)
        b = request.user.id == obj.creator.id

        return request.user.is_authenticated and (is_lead or a or b)
