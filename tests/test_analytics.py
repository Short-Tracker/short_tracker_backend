import pytest

from http import HTTPStatus
from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db(transaction=True)
class TestTaskAnalytics:
    base_url = '/api/v1/task-analytics/'
    periods = [
        ("week", "53.2"),
        ("month", "2"),
        ("custom", "2024-02-01,2024-02-15"),
    ]

    @pytest.mark.parametrize("period_type, period_value", periods)
    def test_analytics_endpoint(
        self, team_lead_client, task, period_type, period_value
    ):
        performer = task.performers.all()[0]
        custom_url = self.build_url(
            performer.id, period_type, period_value)
        response = team_lead_client.get(custom_url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что GET-запрос авторизованного пользователя к `{custom_url}` возвращает статус 200.'
        )

        data = response.json()
        assert isinstance(data, dict), (
            'Проверьте, что GET-запрос тимлида к '
            f'`{custom_url}` возвращает список.'
        )

    @pytest.mark.parametrize("period_type, period_value", periods)
    def test_perform_access(
            self, performer_client, task, period_type, period_value
    ):
        performer = task.performers.all()[0]
        custom_url = self.build_url(performer.id, period_type, period_value)
        response = performer_client.get(custom_url)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Проверьте, что GET-запрос пользователю без прав доступа возвращает статус 403.'
        )

    def build_url(self, performer_id, period_type, period_value):
        if period_type == "custom":
            start_date, end_date = period_value.split(',')
            return (
                f"{self.base_url}?performer_id={performer_id}"
                f"&start_date={start_date}&end_date={end_date}"
            )
        else:
            return (
                f"{self.base_url}?performer_id={performer_id}"
                f"&{period_type}={period_value}"
            )
