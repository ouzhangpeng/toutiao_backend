"""
Unit tests for history functionality
"""

import pytest
from httpx import AsyncClient


class TestHistoryAdd:
    """Tests for adding history"""

    @pytest.mark.asyncio
    async def test_add_history_not_logged_in(self, client: AsyncClient):
        """Test add history without login"""
        response = await client.post("/api/history/add", json={"newsId": 1})
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_add_history_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test add history successfully"""
        response = await client.post(
            "/api/history/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


class TestHistoryList:
    """Tests for history list retrieval"""

    @pytest.mark.asyncio
    async def test_get_history_list_not_logged_in(self, client: AsyncClient):
        """Test get history list without login"""
        response = await client.get("/api/history/list")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_history_list(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test get history list"""
        # First add some history
        await client.post(
            "/api/history/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        response = await client.get(
            "/api/history/list", headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]


class TestHistoryDelete:
    """Tests for deleting history"""

    @pytest.mark.asyncio
    async def test_delete_history_not_logged_in(self, client: AsyncClient):
        """Test delete history without login"""
        response = await client.delete("/api/history/delete/1")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_history_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test delete history successfully"""
        # First add some history
        await client.post(
            "/api/history/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        # Get history list to find an id
        list_response = await client.get(
            "/api/history/list", headers={"Authorization": f"Bearer {test_user_token}"}
        )
        history_list = list_response.json()["data"]["list"]

        if history_list:
            history_id = history_list[0]["id"]
            # Delete the history
            response = await client.delete(
                f"/api/history/delete/{history_id}",
                headers={"Authorization": f"Bearer {test_user_token}"},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200


class TestHistoryClear:
    """Tests for clearing history"""

    @pytest.mark.asyncio
    async def test_clear_history_not_logged_in(self, client: AsyncClient):
        """Test clear history without login"""
        response = await client.delete("/api/history/clear")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_clear_history_success(
        self, client: AsyncClient, test_user_token: str, test_data
    ):
        """Test clear history successfully"""
        # First add some history
        await client.post(
            "/api/history/add",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"newsId": test_data["news1"].id},
        )

        response = await client.delete(
            "/api/history/clear", headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
