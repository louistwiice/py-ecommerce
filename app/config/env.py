import os

REDIS_URL = os.getenv("REDIS_URL", default="redis://redis:6379/")
REDIS_DEFAULT_DB = int(os.getenv("REDIS_DEFAULT_DB", default=2))

