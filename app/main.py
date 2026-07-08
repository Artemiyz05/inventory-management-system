from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router

from app.models.types import Type
from app.models.users import User

from contextlib import asynccontextmanager
from app.database import engine, Model

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield

    print("Выключение сервера")


app = FastAPI(lifespan=lifespan)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(auth_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
