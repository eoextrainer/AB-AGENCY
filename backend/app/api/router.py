from fastapi import APIRouter

from app.api.routes import artists, auth, dashboard, inquiries, public

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
api_router.include_router(artists.router, prefix="/artists", tags=["artists"])
api_router.include_router(inquiries.router, prefix="/inquiries", tags=["inquiries"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
