import os

import fakeredis
import redis
from django.conf import settings

redis = (
    fakeredis.FakeStrictRedis()
    if settings.DEV is True
    else redis.Redis(host="localhost", port="6379", password=os.environ["RULE_DB"])
)
