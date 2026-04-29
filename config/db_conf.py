from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 从配置模块读取数据库 URL
from .settings import settings

# 根据配置获取数据库连接 URL
ASYNC_DATABASE_URL = settings.ASYNC_DATABASE_URL

# SQLite 不支持连接池参数
is_sqlite = ASYNC_DATABASE_URL.startswith("sqlite")
engine_kwargs = {}
if not is_sqlite:
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20


# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=not is_sqlite,  # SQLite 不输出日志
    **engine_kwargs,
)

# 创建异步工厂
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 获取会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
