from fastapi import FastAPI
from src.routers import user_router, ecg_router

app = FastAPI()

app.title = "Idoven Challenge"
app.version = "0.1"
app.include_router(router=user_router.router)
app.include_router(router=ecg_router.router)
