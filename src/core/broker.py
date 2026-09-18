import taskiq_fastapi
from taskiq import SmartRetryMiddleware, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from src.core.config import settings

schedule_source = ListRedisScheduleSource(
    url=settings.redis.REDIS_URL,
    max_connection_pool_size=settings.redis.CONNECTION_POOL_MAXSIZE,
)

broker = ListQueueBroker(
    url=settings.redis.REDIS_URL,
    queue_name="crypto",
    max_connection_pool_size=settings.redis.CONNECTION_POOL_MAXSIZE,
).with_middlewares(
    SmartRetryMiddleware(
        default_retry_count=settings.taskiq.TASKIQ_RETRY_COUNT,
        default_delay=settings.taskiq.TASKIQ_RETRY_DELAY,
        schedule_source=schedule_source,
    ),
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker), schedule_source],
)

taskiq_fastapi.init(broker, "src.main:app")
