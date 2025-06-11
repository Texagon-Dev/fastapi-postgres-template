from fastapi import FastAPI, APIRouter
from app.features.auth.router import router as auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)

def register_routes(app: FastAPI):
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    app.include_router(api_router)