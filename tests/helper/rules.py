def new_rule(priority=5):
    return {'ruleId': '',
            'accountId': '3456',
            'priority': priority,
            'rule': {
                'filters': {
                    'fromAddress': ["a@b"],
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
