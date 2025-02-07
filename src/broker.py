from environs import Env
from taskiq_redis import ListQueueBroker

from src.config import RedisConfig

env = Env()
env.read_env()


redis_config = RedisConfig.from_env(env)

broker = ListQueueBroker(redis_config.construct_redis_dsn)
