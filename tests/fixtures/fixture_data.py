from datetime import date, timedelta

import pytest

from tasks.models import Task


@pytest.fixture
def create_task(user_1, team_lead_user):
    def _create_task(creator, performers, has_deadline):
        create_date = date.today() - timedelta(days=15)
        inprogress_date = create_date + timedelta(days=4)
        done_date = inprogress_date + timedelta(days=2)
        creator_user = user_1 if creator == 'user_1' else team_lead_user
        performers_users = [
            team_lead_user
            if performer == 'team_lead'
            else user_1 for performer in performers]
        deadline_date = (
            done_date - timedelta(days=1)
            if has_deadline else done_date + timedelta(days=3))
        task_data = Task.objects.create(
            creator=creator_user,
            link="https://short-tracker.acceleratorpracticum.ru/",
            description=(
                f'Task {"with" if has_deadline else "without"} deadline'),
            status=Task.TaskStatus.DONE,
            create_date=create_date,
            inprogress_date=inprogress_date,
            done_date=done_date,
            deadline_date = deadline_date,
            get_medals=True,
        )
        task_data.performers.set(performers_users)
        return task_data
    return _create_task


@pytest.fixture
def tasks(create_task):
    return [
        create_task('user_1', 'user_1', True),
        create_task('team_lead_user', 'user_1', True),
        create_task('team_lead_user', 'user_1', False),
        create_task('team_lead_user', 'user_1', False),
        create_task('team_lead_user', 'user_1', False),
    ]
