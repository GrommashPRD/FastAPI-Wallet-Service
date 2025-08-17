import pytest
from httpx import AsyncClient, ASGITransport


from app.main import app


@pytest.mark.asyncio
async def test_get_wallet_details(new_wallet, authorized_user_empty):
    wallet_uuid = new_wallet["wallet id"]

    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
            cookies=authorized_user_empty) as client:
        response = await client.get(f"api/v1/wallets/{wallet_uuid}/details")

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["message"] == "OK"


@pytest.mark.asyncio
async def test_get_wallet_details_without_auth(
        new_wallet,
        authorized_user_empty
):

    wallet_uuid = new_wallet["wallet id"]

    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test") as client:
        response = await client.get(f"api/v1/wallets/{wallet_uuid}/details")

        assert response.status_code == 401
        response_json = response.json()

        assert response_json["detail"] == "You need authorize for see details"
