from datetime import date, timedelta

import pytest

from tasks.models import Task


@pytest.fixture(params=[
    {'creator': 'user_1', 'performer': 'user_1', 'deadline': True},
    {'creator': 'team_lead_user', 'performer': 'user_1', 'deadline': True},
    {'creator': 'team_lead_user', 'performer': 'user_1', 'deadline': False},
    {'creator': 'team_lead_user', 'performer': 'user_1', 'deadline': False},
])
def task(request, user_1, team_lead_user):
    task_params = request.param
    deadline = (
        date.today() + timedelta(days=7)
        if task_params['deadline'] 
        else date.today() - timedelta(days=7)
    )
    creator_user = (
        user_1
        if task_params['creator'] == 'user'
        else team_lead_user)
    performer_user = (
        team_lead_user
        if task_params['performer'] == 'team_lead'
        else user_1)
    task = Task.objects.create(
        creator=creator_user,
        description= (
            f'Task {"with" if task_params["deadline"] else "without"} '
            f'deadline'),
            deadline_date=deadline,
            status=Task.TaskStatus.DONE,
    )
    task.performers.set([performer_user])
    return task
