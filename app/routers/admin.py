from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from starlette.status import HTTP_303_SEE_OTHER

from typing import Annotated

from sqlalchemy import select

from app.dependencies.auth import check_auth

from app.database import SessionDep

from app.models.types import Type
from app.models.users import User

from app.core.security import hash_password

router = APIRouter(
    prefix="/admin", tags=["Администратор"], dependencies=[Depends(check_auth)]
)

templates = Jinja2Templates(directory="app/templates")


async def get_types(session: SessionDep):
    stmt = select(Type)
    result = await session.execute(stmt)
    return result.scalars().all()


def validate_user_data(username: str, password: str):
    if len(username) < 5:
        return "Логин должен содержать минимум 5 символов"

    if len(password) < 5:
        return "Пароль должен содержать минимум 5 символов"

    return None


@router.get("/", name="index_page")
async def main(request: Request):
    return templates.TemplateResponse(
        "admin/Index.html",
        {"request": request},
    )


@router.get("/profile", name="profile_page")
async def open_profile(
    request: Request, session: SessionDep, username: str = Depends(check_auth)
):
    stmt = select(User).where(User.login == username)
    result = await session.execute(stmt)
    user = result.scalar_one()
    return templates.TemplateResponse(
        "admin/Profile.html",
        {
            "request": request,
            "user": user,
        },
    )


@router.post("/profile")
async def save_profile(
    request: Request,
    session: SessionDep,
    full_name: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    password: Annotated[str | None, Form()] = None,
    username: str = Depends(check_auth),
):
    if password:
        error = validate_user_data(username, password)

        if error:
            stmt = select(User).where(User.login == username)
            result = await session.execute(stmt)
            user = result.scalar_one()

            return templates.TemplateResponse(
                "admin/Profile.html",
                {
                    "request": request,
                    "user": user,
                    "error": "error",
                },
            )
    stmt = select(User).where(User.login == username)
    result = await session.execute(stmt)
    user = result.scalar_one()

    user.full_name = full_name
    user.email = email
    if password:
        user.password_hash = hash_password(password)
    await session.commit()
    return RedirectResponse(url="/admin/profile", status_code=HTTP_303_SEE_OTHER)


@router.get("/register", name="register_page")
async def open_register(request: Request, session: SessionDep):
    types = await get_types(session)

    return templates.TemplateResponse(
        "admin/Register.html",
        {
            "request": request,
            "types": types,
        },
    )


@router.post("/register")
async def create_user(
    request: Request,
    session: SessionDep,
    full_name: Annotated[str, Form()],
    username: Annotated[str, Form()],
    typeid: Annotated[int, Form()],
    password: Annotated[str, Form()],
):
    types = await get_types(session)
    error = validate_user_data(username, password)

    if error:
        return templates.TemplateResponse(
            "admin/Register.html",
            {
                "request": request,
                "types": types,
                "error": "error",
            },
        )

    stmt = select(User).where(User.login == username)

    result = await session.execute(stmt)

    existing_user = result.scalar_one_or_none()

    if existing_user:
        return templates.TemplateResponse(
            "admin/Register.html",
            {
                "request": request,
                "types": types,
                "error": "Такой логин уже существует",
            },
        )

    hashed_password = hash_password(password)
    user = User(
        full_name=full_name,
        login=username,
        password_hash=hashed_password,
        typeid=typeid,
    )

    session.add(user)
    await session.commit()

    return RedirectResponse(url="/admin/register", status_code=HTTP_303_SEE_OTHER)


@router.get("/parts_in_stock", name="parts_in_stock_page")
async def open_parts_in_stock(
    request: Request, session: SessionDep, username: str = Depends(check_auth)
):
    return templates.TemplateResponse(
        "admin/Parts_in_stock.html",
        {
            "request": request,
        },
    )


@router.get("/supplier", name="supplier_page")
async def open_supplier(
    request: Request, session: SessionDep, username: str = Depends(check_auth)
):
    return templates.TemplateResponse(
        "admin/Supplier.html",
        {
            "request": request,
        },
    )
