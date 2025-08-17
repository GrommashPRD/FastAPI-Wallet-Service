import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app


@pytest.mark.asyncio
async def test_get_wallet_success(authorized_user):
    client_cookies = Cookies(authorized_user)
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
            cookies=client_cookies) as client:
        response = await client.get("api/v1/wallets/my/")

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["message"] == "OK"


@pytest.mark.asyncio
async def test_get_wallet_without_auth(created_user):

    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test") as client:
        response = await client.get("api/v1/wallets/my/")

        assert response.status_code == 401
        response_json = response.json()

        assert response_json["detail"] == "You need authorize for see wallets"
