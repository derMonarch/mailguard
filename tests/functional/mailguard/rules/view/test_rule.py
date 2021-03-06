from rest_framework.test import APITestCase
from tests.helper.decoding import get_dict
from tests.helper.rules import new_rule, invalid_rule


class RuleViewTest(APITestCase):
    rules_url = '/api/v1/rules/'
    tasks_rules_url = '/api/v1/rules/tasks/'
    tasks_url = '/api/v1/tasks/'

    def test_post_new_rule(self):
        response = self.client.post(self.rules_url, new_rule(), format='json')
        response_data = get_dict(response)

        assert response.status_code == 201
        assert response_data['ruleId'] is not None
        assert response_data['priority'] == 5
        assert response_data['accountId'] in '3456'
        assert response_data['rule']['filters']['fromAddress'][0] in 'a@b'
        assert response_data['rule']['filters']['words'][0] in 'winning'
        assert response_data['rule']['filters']['links'][0] in 'https://google.com'
        assert response_data['rule']['filters']['tags']['categories'][0] in 'gaming'
        assert response_data['rule']['filters']['tags']['subjects'][0] in 'lottery'
        assert response_data['rule']['filters']['tags']['sentiment'][0] in 'happy'
        assert response_data['rule']['filters']['tags']['buzzwords'][0] in 'money'
        assert response_data['rule']['filters']['tags']['summary'][0] in 'won the lottery'
        assert response_data['rule']['actions']['delete'] is False
        assert response_data['rule']['actions']['copy'] is False
        assert response_data['rule']['actions']['forward'][0] in 'a@b'
        assert response_data['rule']['actions']['moveTo'][0] in 'firma'
        assert response_data['rule']['actions']['encryption']['encrypt'] is True
        assert response_data['rule']['actions']['encryption']['method'][0] in 'subject_and_body'

    def test_post_new_rule_invalid(self):
        response = self.client.post(self.rules_url, invalid_rule(), format='json')
        response_data = get_dict(response)

        assert response_data['status'] in 'error'
        assert response_data['message'] is not None

    def test_post_link_task_to_rule(self):
        created_task = self.client.post(self.tasks_url, self._new_task(), format='json')
        created_rule = self.client.post(self.rules_url, new_rule(), format='json')
        task = get_dict(created_task)
        rule = get_dict(created_rule)

        payload = {'account_id': '3456',
                   'task_id': task['id'],
                   'rule_id': rule['ruleId']}

        created_rule = self.client.post(self.tasks_rules_url, payload, format='json')
        task_rule = get_dict(created_rule)

        assert task_rule['id'] == 1
        assert task_rule['account_id'] in '3456'
        assert task_rule['task_id'] == 1
        assert task_rule['rule_id'] is not None

    @staticmethod
    def _new_task():
        return {'account_id': '3456',
                'time_interval': 4,
                'priority': 5}
