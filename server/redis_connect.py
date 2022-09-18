from redis_om import get_redis_connection, HashModel
from config import config


redis = get_redis_connection(
  host=config.redis_host,
  port=config.redis_port,
  password=config.redis_password,
  decode_responses=True
)


class Delivery(HashModel):
  budget: int = 0
  notes: str = ''

  class Meta:
    database = redis


class Event(HashModel):
  delivery_id: str = ''
  type: str = ''
  data: str = ''

  class Meta:
    database = redis