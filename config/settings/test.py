"""
测试环境配置
"""

from .base import Settings


class TestSettings(Settings):
    DEBUG: bool = True

    # 测试环境使用 SQLite 内存数据库
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    # 测试环境使用不同的 Redis 数据库
    REDIS_DB: int = 15

    # SQLAlchemy 配置
    SQLALCHEMY_ECHO: bool = False
