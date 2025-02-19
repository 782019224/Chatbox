from apscheduler.jobstores import redis

import redis

r = redis.Redis(
    host='redis-17683.c74.us-east-1-4.ec2.redns.redis-cloud.com',
    REDISPORT=17683,
    username="default",
    password="mweRdf42p0RbDMw1Ja8KNXp6AWORqjsL",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)

