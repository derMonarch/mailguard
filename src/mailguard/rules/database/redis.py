import os

import fakeredis
import redis
from django.conf import settings

redis = (
    fakeredis.FakeStrictRedis()
    if settings.DEV is True
    else redis.Redis(
        host=os.environ["RULE_DB_HOST"],
        port=os.environ["RULE_DB_PORT"],
        password=os.environ['RULE_DB_PASSWORD']
    )
)
