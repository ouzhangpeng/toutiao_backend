"""
开发环境配置
"""

from .base import Settings


class DevelopmentSettings(Settings):
    DEBUG: bool = True

    # 开发环境数据库配置
    DB_NAME: str = "news_app"

    # 开发环境 Redis 配置
    REDIS_DB: int = 0

    # SQLAlchemy 配置
    SQLALCHEMY_ECHO: bool = True
