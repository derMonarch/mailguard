import ast
import json
from rest_framework.test import APITestCase


class RuleViewTest(APITestCase):
    rules_url = "/api/v1/rules/"
    tasks_url = "/api/v1/rules/tasks/"

    def test_post_new_rule(self):
        response = self.client.post(self.rules_url, self._new_rule(), format='json')
        decoded_str = response.content.decode('utf8')
        response_data = json.loads(decoded_str)

        assert response.status_code == 201
        assert response_data['ruleId'] is not None
        assert response_data['accountId'] in '3456'
        assert response_data['rule']['filters']['fromAddress'][0] in 'a@b'
        assert response_data['rule']['filters']['tags']['categories'][0] in 'gaming'
        assert response_data['rule']['delete'] is False
        assert response_data['rule']['moveTo'][0] in 'firma'
        assert response_data['rule']['encrypt'] is False
        assert response_data['rule']['message'][0] in 'subject'

    @staticmethod
    def _new_rule():
        return {'ruleId': '1234',
                'accountId': '3456',
                'rule': {
                    'filters': {
                        'fromAddress': ["a@b"],
                        'tags': {
                            'categories': ['gaming']
                        }
                    },
                    'delete': False,
                    'moveTo': ["firma"],
                    'encrypt': False,
                    'message': ["subject"]
                }}
