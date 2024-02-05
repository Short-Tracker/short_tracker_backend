from http import HTTPStatus

import pytest

from users.models import CustomUser


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

    def build_url(self, start_date=None, end_date=None):
        url = f"{self.base_url}?"
        if start_date:
            url += f"start_date={start_date}"
            if end_date:
                url += f"&end_date={end_date}"
        return url

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
        non_lead_users = CustomUser.objects.filter(
            is_team_lead=False)
        for performer_id in data.get('performers_analytics', {}):
            assert performer_id in map(
                str, non_lead_users.values_list('id', flat=True)
                ), (
                    'Убедитесь, что в аналитике отсутствуют лиды.')
  
    def test_perform_access(
            self, performer_client):
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
        response = performer_client.post(custom_url)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что POST-запрос пользователю без прав к '
            f'`{custom_url}` возвращает ответ со статусом 403.'
        )

    def test_access_not_auth(
            self, client):
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
        response = client.post(custom_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            f'`{custom_url}` возвращает ответ со статусом 401.'
        )
