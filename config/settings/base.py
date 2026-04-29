"""
基础配置类 - 包含所有环境共享的配置
"""

from typing import Optional


class Settings:
    # 应用配置
    APP_NAME: str = "toutiao-backend"
    DEBUG: bool = False

    # 数据库配置
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "helloworld"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "news_app"
    DB_CHARSET: str = "utf8"

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # SQLAlchemy 配置
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_POOL_SIZE: int = 10
    SQLALCHEMY_MAX_OVERFLOW: int = 20

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """构造数据库连接 URL"""
        return f"mysql+aiomysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
