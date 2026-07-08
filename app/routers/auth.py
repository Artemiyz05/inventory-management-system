from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from sqlalchemy import select
from passlib.context import CryptContext

from app.database import SessionDep
from app.models.users import User

from app.dependencies.auth import create_access_token

from app.core.security import verify_password


router = APIRouter(prefix="/auth", tags=["Авторизация"])

templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.get("/", name="auth_index_page")
async def open_login(request: Request):
    return templates.TemplateResponse(
        "auth/Login.html",
        {"request": request},
    )


@router.post("/")
async def open_admin(
    request: Request,
    session: SessionDep,
    username: str = Form(...),
    password: str = Form(...),
):
    stmt = select(User).where(User.login == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return templates.TemplateResponse(
            "auth/Login.html",
            {"request": request, "error": "Пользователь не найден"},
        )

    if not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/Login.html",
            {"request": request, "error": "Неверный пароль"},
        )

    access_token = create_access_token(
        data={
            "sub": user.login,
            "user_id": user.iduser,
        }
    )

    response = RedirectResponse(url="/admin/", status_code=HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )

    return response


@router.get("/logout", name="logout")
async def logout():

    response = RedirectResponse(url="/auth/", status_code=303)

    response.delete_cookie("access_token")

    return response
