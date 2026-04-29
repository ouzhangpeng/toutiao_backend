"""
Unit tests for favorite functionality
"""

import pytest
from httpx import AsyncClient


class TestFavoriteCheck:
    """Tests for favorite status check"""

    @pytest.mark.asyncio
    async def test_check_favorite_not_logged_in(self, client: AsyncClient):
        """Test check favorite without login"""
        response = await client.get("/api/favorite/check?newsId=1")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_check_favorite_logged_in(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test check favorite with login"""
        response = await client.get(
            f"/api/favorite/check?newsId={test_data['news1'].id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "isFavorite" in data["data"]


class TestFavoriteAdd:
    """Tests for adding favorites"""

    @pytest.mark.asyncio
    async def test_add_favorite_not_logged_in(self, client: AsyncClient):
        """Test add favorite without login"""
        response = await client.post("/api/favorite/add", json={"newsId": 1})
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_add_favorite_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test add favorite successfully"""
        response = await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    @pytest.mark.asyncio
    async def test_add_duplicate_favorite(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test adding same favorite twice"""
        # Add first time
        await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news2"].id},
        )

        # Add second time
        response = await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news2"].id},
        )
        # Should handle gracefully (either success or error)
        assert response.status_code in [200, 400]


class TestFavoriteRemove:
    """Tests for removing favorites"""

    @pytest.mark.asyncio
    async def test_remove_favorite_not_logged_in(self, client: AsyncClient):
        """Test remove favorite without login"""
        response = await client.delete("/api/favorite/remove?newsId=1")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_remove_favorite_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test remove favorite successfully"""
        # First add a favorite
        await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        # Then remove it
        response = await client.delete(
            f"/api/favorite/remove?newsId={test_data['news1'].id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


class TestFavoriteList:
    """Tests for favorite list retrieval"""

    @pytest.mark.asyncio
    async def test_get_favorite_list_not_logged_in(self, client: AsyncClient):
        """Test get favorite list without login"""
        response = await client.get("/api/favorite/list")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_favorite_list(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test get favorite list"""
        # Add some favorites first
        await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        response = await client.get(
            "/api/favorite/list", headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]


class TestFavoriteClear:
    """Tests for clearing favorites"""

    @pytest.mark.asyncio
    async def test_clear_favorites_not_logged_in(self, client: AsyncClient):
        """Test clear favorites without login"""
        response = await client.delete("/api/favorite/clear")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_clear_favorites_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test clear favorites successfully"""
        # Add some favorites first
        await client.post(
            "/api/favorite/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        response = await client.delete(
            "/api/favorite/clear",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
