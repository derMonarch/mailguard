from rest_framework.test import APITestCase
from tests.helper.decoding import get_dict


class TasksViewTest(APITestCase):
    tasks_url = '/api/v1/tasks/'

    def test_post_new_task(self):
        response = self.client.post(self.tasks_url, self._new_task(), format='json')
        response_data = get_dict(response)

        assert response.status_code == 201
        assert response_data['account_id'] in '3456'
        assert response_data['time_interval'] == 4
        assert response_data['priority'] == 5
        assert response_data['active'] is False
        assert response_data['state'] in 'OK'

    @staticmethod
    def _new_task():
        return {'account_id': '3456',
                'time_interval': 4,
                'priority': 5}
