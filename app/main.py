from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.handlers.auth.router import router as auth_router
from app.api.handlers.wallets.router import router as wallet_router


app = FastAPI()
app.include_router(auth_router, prefix="/api/v1")
app.include_router(wallet_router, prefix="/api/v1")


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"
