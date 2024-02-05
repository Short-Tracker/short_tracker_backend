from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestTaskAnalytics:
    base_url = '/api/v1/task-analytics/'
    periods = [
        ("2024-02-01", "2024-02-15"),
        ("2023-02-10", "2023-02-20"),
        ("2022-02-01", "2023-02-15"),
        ("2023-02-10", "2024-02-20"),
        ("", "2023-05-28"),
        ("2023-12-01", "")
    ]

    def build_url(self, start_date, end_date):
        return (
                f"{self.base_url}?&{start_date}&end_date={end_date}"
            )

    @pytest.mark.parametrize("start_date, end_date", periods)
    def test_analytics_endpoint(
        self, team_lead_client, task, start_date, end_date
    ):

        custom_url = self.build_url(
            start_date=start_date, end_date=end_date)
        response = team_lead_client.get(custom_url)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'{custom_url}` возвращает статус 200.'
        )

        data = response.json()
        assert isinstance(data, dict), (
            'Проверьте, что GET-запрос тимлида к '
            f'`{custom_url}` возвращает список.'
        )

    @pytest.mark.parametrize("start_date, end_date", periods)
    def test_perform_access(
            self, performer_client, task, start_date, end_date
    ):
        custom_url =  self.build_url(
            start_date=start_date, end_date=end_date)
        response = performer_client.get(custom_url)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что GET-запрос пользователю без прав '
            'доступа возвращает статус 403.'
        )
