"""
Unit tests for news functionality
"""

import pytest
from httpx import AsyncClient


class TestNewsCategories:
    """Tests for news categories"""

    @pytest.mark.asyncio
    async def test_get_categories(self, client: AsyncClient):
        """Test getting news categories"""
        response = await client.get("/api/news/categories")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert isinstance(data["data"], list)


class TestNewsList:
    """Tests for news list retrieval"""

    @pytest.mark.asyncio
    async def test_get_news_list(self, client: AsyncClient, test_data):
        """Test getting news list"""
        response = await client.get(
            f"/api/news/list?categoryId={test_data['category1'].id}&page=1&pageSize=10"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert "hasMore" in data["data"]

    @pytest.mark.asyncio
    async def test_get_news_list_with_category(self, client: AsyncClient, test_data):
        """Test getting news list with category filter"""
        response = await client.get(
            f"/api/news/list?categoryId={test_data['category1'].id}&page=1&pageSize=10"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert "list" in data["data"]

    @pytest.mark.asyncio
    async def test_get_news_list_pagination(self, client: AsyncClient, test_data):
        """Test news list pagination"""
        response = await client.get(
            f"/api/news/list?categoryId={test_data['category1'].id}&page=1&pageSize=10"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert "list" in data["data"]


class TestNewsDetail:
    """Tests for news detail retrieval"""

    @pytest.mark.asyncio
    async def test_get_news_detail(self, client: AsyncClient, test_data):
        """Test getting news detail"""
        response = await client.get(f"/api/news/detail?id={test_data['news1'].id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "data" in data
        assert data["data"]["id"] == test_data["news1"].id
        assert "title" in data["data"]
        assert "content" in data["data"]

    @pytest.mark.asyncio
    async def test_get_nonexistent_news(self, client: AsyncClient):
        """Test getting non-existent news"""
        response = await client.get("/api/news/detail?id=99999")
        assert response.status_code == 404
