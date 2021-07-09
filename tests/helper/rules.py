from mailguard.rules.services import basic as rule_service
from mailguard.rules.models.rule_task_model import TaskToRuleModel


def new_rule(priority=5):
    return {'ruleId': '',
            'accountId': '3456',
            'priority': priority,
            'rule': {
                'filters': {
                    'fromAddress': ['a@b'],
                    'words': ['winning'],
                    'links': ['https://google.com'],
                    'tags': {
                        'categories': ['gaming'],
                        'subjects': ['lottery'],
                        'sentiment': ['happy'],
                        'buzzwords': ['money'],
                        'summary': ['won the lottery']
                    }
                },
                'actions': {
                    'delete': False,
                    'copy': False,
                    'moveTo': ['firma'],
                    'forward': ['a@b'],
                    'encryption': {
                        'encrypt': True,
                        'method': ['subject_and_body']
                    }
                }
            }}


def new_custom_rule(priority=5, from_address='a@b', move_to='firma'):
    return {'ruleId': '',
            'accountId': '3456',
            'priority': priority,
            'rule': {
                'filters': {
                    'fromAddress': [from_address]
                },
                'actions': {
                    'moveTo': [move_to]
                }
            }}


def invalid_rule():
    return {'ruleId': '',
            'accountId': '3456',
            'rule': {
                'filters': {
                    'fromAddress': ["a@b"],
                    'words': ['winning'],
                    'links': ['https://google.com']
                },
                'actions': {
                    'delete': False,
                    'copy': False,
                    'moveTo': ['firma'],
                    'forward': ['a@b']
                }
            }}


def add_rules_to_task_db(account_id, created_task):
    rule = rule_service.create_new_rule(new_custom_rule(priority=1))
    rule_two = rule_service.create_new_rule(new_custom_rule(priority=3, from_address='b@a', move_to='spam'))
    rule_three = rule_service.create_new_rule(new_custom_rule(priority=5, from_address='hello@goodbye', move_to='spam'))

    TaskToRuleModel.objects.create(
        account_id=account_id,
        task_id=created_task.id,
        rule_id=rule['ruleId']
    )

    TaskToRuleModel.objects.create(
        account_id=account_id,
        task_id=created_task.id,
        rule_id=rule_two['ruleId']
    )

    TaskToRuleModel.objects.create(
        account_id=account_id,
        task_id=created_task.id,
        rule_id=rule_three['ruleId']
    )
