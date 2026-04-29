"""
pytest configuration and fixtures for the toutiao-backend project
"""

import os

# 在导入任何配置模块之前设置测试环境变量
os.environ["APP_ENV"] = "test"

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.base import Base
from models.news import News, Category

# 从配置模块读取测试数据库 URL
from config.settings import settings

# 使用配置中的数据库 URL（测试环境会使用 SQLite 内存数据库）
TEST_DATABASE_URL = settings.ASYNC_DATABASE_URL

# 创建测试用的数据库引擎和会话
_test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
_test_session_maker = async_sessionmaker(_test_engine, expire_on_commit=False)


async def get_test_db():
    """Dependency for test database session"""
    async with _test_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def setup_database():
    """Setup database tables for each test (clean slate)"""
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_database):
    """Create a new database session for each test"""
    async with _test_session_maker() as session:
        yield session


@pytest.fixture
async def client(setup_database):
    """Create an async HTTP client for testing"""
    from main import app
    from config.db_conf import get_db

    # 覆盖数据库依赖
    app.dependency_overrides[get_db] = get_test_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # 清理依赖覆盖
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user_token(client):
    """Register and login a test user, return token"""
    register_response = await client.post(
        "/api/users/register", json={"username": "testuser", "password": "testpass123"}
    )
    assert (
        register_response.status_code == 200
    ), f"Register failed: {register_response.content}"

    login_response = await client.post(
        "/api/users/login", json={"username": "testuser", "password": "testpass123"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.content}"
    return login_response.json()["data"]["token"]


@pytest.fixture
async def test_data(db_session):
    """Create test data (categories and news)"""
    from datetime import datetime

    # Create categories
    category1 = Category(name="科技", sort_order=1)
    category2 = Category(name="体育", sort_order=2)
    db_session.add(category1)
    db_session.add(category2)
    await db_session.flush()

    # Create news
    news1 = News(
        title="测试新闻1",
        description="测试描述1",
        content="测试内容1",
        image="https://example.com/image1.jpg",
        author="测试作者",
        category_id=category1.id,
        views=100,
        publish_time=datetime.now(),
    )
    news2 = News(
        title="测试新闻2",
        description="测试描述2",
        content="测试内容2",
        image="https://example.com/image2.jpg",
        author="测试作者",
        category_id=category2.id,
        views=200,
        publish_time=datetime.now(),
    )
    db_session.add(news1)
    db_session.add(news2)
    await db_session.commit()
    await db_session.refresh(news1)
    await db_session.refresh(news2)

    return {
        "category1": category1,
        "category2": category2,
        "news1": news1,
        "news2": news2,
    }
