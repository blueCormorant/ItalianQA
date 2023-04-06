import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default-key"
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes in seconds