"""
Unit tests for user authentication and management
"""

import pytest
from httpx import AsyncClient


class TestUserRegistration:
    """Tests for user registration functionality"""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration"""
        response = await client.post(
            "/api/users/register",
            json={"username": "newuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]
        assert "userInfo" in data["data"]
        assert data["data"]["userInfo"]["username"] == "newuser"

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client: AsyncClient):
        """Test registration with existing username"""
        await client.post(
            "/api/users/register",
            json={"username": "duplicate", "password": "password123"},
        )

        response = await client.post(
            "/api/users/register",
            json={"username": "duplicate", "password": "password456"},
        )
        # API直接返回400
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_register_empty_fields(self, client: AsyncClient):
        """Test registration with empty fields"""
        response = await client.post(
            "/api/users/register", json={"username": "", "password": ""}
        )
        # 验证失败返回422
        assert response.status_code == 422


class TestUserLogin:
    """Tests for user login functionality"""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient):
        """Test successful login"""
        await client.post(
            "/api/users/register",
            json={"username": "loginuser", "password": "password123"},
        )

        response = await client.post(
            "/api/users/login",
            json={"username": "loginuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]
        assert "userInfo" in data["data"]

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: AsyncClient):
        """Test login with wrong password"""
        await client.post(
            "/api/users/register",
            json={"username": "wrongpass", "password": "correctpass"},
        )

        response = await client.post(
            "/api/users/login", json={"username": "wrongpass", "password": "wrongpass"}
        )
        # API直接返回401
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user"""
        response = await client.post(
            "/api/users/login",
            json={"username": "nonexistent", "password": "password123"},
        )
        # API直接返回401
        assert response.status_code == 401


class TestUserInfo:
    """Tests for user information retrieval"""

    @pytest.mark.asyncio
    async def test_get_user_info_with_token(
        self, client: AsyncClient, test_user_token: str
    ):
        """Test get user info with valid token"""
        response = await client.get(
            "/api/users/info", headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_info_without_token(self, client: AsyncClient):
        """Test get user info without token"""
        response = await client.get("/api/users/info")
        # 422 表示请求参数验证失败（缺少 token）
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_user_info_invalid_token(self, client: AsyncClient):
        """Test get user info with invalid token"""
        response = await client.get(
            "/api/users/info", headers={"Authorization": "Bearer invalid_token_123"}
        )
        # API直接返回401
        assert response.status_code == 401


class TestUserUpdate:
    """Tests for user profile update"""

    @pytest.mark.asyncio
    async def test_update_user_info(self, client: AsyncClient, test_user_token: str):
        """Test update user information"""
        response = await client.put(
            "/api/users/update",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"bio": "Hello World", "gender": "male"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


class TestPasswordChange:
    """Tests for password change functionality"""

    @pytest.mark.asyncio
    async def test_change_password_success(
        self, client: AsyncClient, test_user_token: str
    ):
        """Test successful password change"""
        response = await client.put(
            "/api/users/password",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"oldPassword": "testpass123", "newPassword": "newpass456"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

        login_response = await client.post(
            "/api/users/login", json={"username": "testuser", "password": "newpass456"}
        )
        assert login_response.status_code == 200
        assert login_response.json()["code"] == 200

    @pytest.mark.asyncio
    async def test_change_password_invalid_old(
        self, client: AsyncClient, test_user_token: str
    ):
        """Test password change with wrong old password"""
        response = await client.put(
            "/api/users/password",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json={"oldPassword": "wrongpass", "newPassword": "newpass456"},
        )
        # 原密码错误返回400
        assert response.status_code == 400
