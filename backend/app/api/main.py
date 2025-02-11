from fastapi import APIRouter
from app.api.routes import login, users, utils, private, items, dns_records

# Consolidated router for all endpoints
api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(private.router, tags=["private"])
api_router.include_router(dns_records.router, prefix="/dns", tags=["dns"])
