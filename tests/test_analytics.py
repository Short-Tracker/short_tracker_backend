from datetime import datetime, timedelta
from http import HTTPStatus

import pytest

from users.models import CustomUser


@pytest.mark.django_db(transaction=True)
class TestTaskAnalytics:
    base_url = '/api/v1/task-analytics/'
    periods = [
        ("2023-02-10", "2024-02-20"),
        ("", "2023-05-28"),
        ("2023-12-01", ""),
        ("", "")
    ]

    def build_url(self, start_date=None, end_date=None):
        url = f"{self.base_url}?"
        if start_date:
            url += f"start_date={start_date}"
            if end_date:
                url += f"&end_date={end_date}"
        return url

    @pytest.mark.parametrize("start_date, end_date", periods)
    def test_analytics_endpoint(
        self, team_lead_client, tasks, start_date, end_date
    ):

        custom_url = self.build_url(
            start_date=start_date, end_date=end_date)
        response = team_lead_client.get(custom_url)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'{custom_url}` возвращает статус 200.'
        )
        data =response.json()
        assert isinstance(data, dict), (
            'Проверьте, что GET-запрос тимлида возвращает словарь.'
        )
  
    def test_perform_access(
            self, performer_client, tasks):
        custom_url = self.build_url()
        assert_msg = (
            'Проверьте, что GET-запрос пользователю без прав к '
            f'`{custom_url}` возвращает ответ со статусом 403.'
        )
        try:
            response = performer_client.get(custom_url)
        except TypeError as error:
            raise AssertionError(
                assert_msg + (
                    f' В процессе выполнения запроса произошла ошибка: {error}'
                )
            )
        assert response.status_code == HTTPStatus.FORBIDDEN, assert_msg

    def test_access_not_auth(
            self, client, tasks):
        custom_url = self.build_url()
        assert_msg = (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{custom_url}` возвращает ответ со статусом 401.'
        )
        try:
            response = client.get(custom_url)
        except TypeError as error:
            raise AssertionError(
                assert_msg + (
                    f' В процессе выполнения запроса произошла ошибка: {error}'
                )
            )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, assert_msg

    def test_analytics_data(self,
                        team_lead_client,
                        tasks,
                        performers_analytics=None):
        response = team_lead_client.get(self.build_url())
        data = response.json()
        expected_fields = (
            'total_tasks_on_time',
            'total_tasks_with_delay',
            'performers_analytics')
        expected_performers_analytics_data = (
            'performer_name',
            'completed_on_time_count',
            'completed_with_delay_count',
            'avg_time_create_date_to_inprogress_date',
            'avg_time_create_date_to_done_date',
            'avg_time_inprogress_date_to_done_date'
        )
        for field in expected_fields:
            assert field in data, (
                'Проверьте, что для лида ответ на '
                f' GET-запрос содержит поле `{field}`.'
            )
        if performers_analytics:
            for field in performers_analytics:
                assert field in expected_performers_analytics_data, (
                'Проверьте, что для лида ответ на '
                f' GET-запрос содержит поле `{field}`.')
            performers_analytics_data = data.get('performers_analytics', {})
            for performer_id in performers_analytics_data:
                performer = CustomUser.objects.get(id=performer_id)
                assert not performer.is_lead, (
                    'Убедитесь, что в аналитике отсутствуют лиды.')

    def test_default_page(self, team_lead_client):
        response = team_lead_client.get(self.build_url())
        expected_tasks = team_lead_client.get(
            self.build_url(
                start_date=datetime.today() - timedelta(days=7)))
        assert len(response.data) == len(expected_tasks.data)
