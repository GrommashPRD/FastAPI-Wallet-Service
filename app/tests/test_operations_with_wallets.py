import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_deposit_wallet(new_wallet, authorized_user_empty):
    wallet_uuid = new_wallet["wallet id"]
    request = {
        "operation": "DEPOSIT",
        "amount": 100
    }
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test") as client:
        response = await client.post(
            f"api/v1/wallets/{wallet_uuid}/operation/",
            json=request
        )

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["message"] == "OK"


@pytest.mark.asyncio
async def test_withdraw_wallet(new_wallet, authorized_user_empty):
    wallet_uuid = new_wallet["wallet id"]
    request = {
        "operation": "WITHDRAW",
        "amount": 50
    }
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
            cookies=authorized_user_empty) as client:
        response = await client.post(
            f"api/v1/wallets/{wallet_uuid}/operation/",
            json=request
        )

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["message"] == "OK"


@pytest.mark.asyncio
async def test_withdraw_wallet_without_auth(new_wallet, authorized_user_empty):
    wallet_uuid = new_wallet["wallet id"]
    request = {
        "operation": "WITHDRAW",
        "amount": 50
    }
    async with (AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test") as client):
        response = await client.post(
            f"api/v1/wallets/{wallet_uuid}/operation/",
            json=request
        )

        assert response.status_code == 401
        response_json = response.json()

        assert response_json["detail"] == "Need authorize for withdraw operation"
