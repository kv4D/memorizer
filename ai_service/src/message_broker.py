from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker
from .configs import service_settings

result_backend = RedisAsyncResultBackend(redis_url=service_settings.RESULT_BACKEND_URL)

message_broker = RedisStreamBroker(
    url=service_settings.MESSAGE_BROKER_URL
).with_result_backend(result_backend)
