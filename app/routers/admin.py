from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from starlette.status import HTTP_303_SEE_OTHER

from typing import Annotated

from sqlalchemy import select, or_, func, union_all, literal, Integer, Date
from sqlalchemy.orm import aliased

from app.dependencies.auth import check_auth

from app.database import SessionDep

from app.models.types import Type
from app.models.users import User
from app.models.suppliers import Supplier
from app.models.details import Detail
from app.models.supplies import Supply
from app.models.future_prices import Future_price
from app.models.history_prices import History_price
from app.schemas.users import SupplierUpdate
from app.schemas.detail import DetailUpdate

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
    type_id: Annotated[int, Form()],
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
        type_id=type_id,
    )

    session.add(user)
    await session.commit()

    return RedirectResponse(url="/admin/register", status_code=HTTP_303_SEE_OTHER)


@router.get("/parts_in_stock", name="parts_in_stock_page")
async def open_parts_in_stock(
    request: Request,
    session: SessionDep,
    username: str = Depends(check_auth),
    search: str | None = None,
):
    stmt = select(
        Detail.iddetails,
        Detail.name,
        Detail.article,
        Detail.price,
        func.sum(Supply.quantity).label("quantity"),
    ).join(Supply, Supply.detail_id == Detail.iddetails)

    if search:
        stmt = stmt.where(
            or_(
                Detail.name.ilike(f"%{search}%"),
                Detail.article.ilike(f"%{search}%"),
            )
        )

    stmt = stmt.group_by(
        Detail.iddetails,
        Detail.name,
        Detail.article,
        Detail.price,
    )
    result = await session.execute(stmt)
    details = result.all()
    return templates.TemplateResponse(
        "admin/Parts_in_stock.html",
        {
            "request": request,
            "details": details,
            "search": search,
        },
    )


@router.put("/parts_in_stock/{detail_id}")
async def update_detail(
    detail_id: int,
    data: DetailUpdate,
    session: SessionDep,
    username: str = Depends(check_auth),
):
    detail = await session.get(Detail, detail_id)

    if detail is None:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    exists = await session.scalar(
        select(Detail.iddetails).where(
            Detail.article == data.article,
            Detail.iddetails != detail_id,
        )
    )
    if exists:
        raise HTTPException(status_code=400, detail="Артикул уже существует")

    detail.name = data.name
    detail.article = data.article
    detail.price = data.price
    detail.note = data.note

    await session.commit()
    await session.refresh(detail)

    return {"message": "OK"}


@router.get("/supplier", name="supplier_page")
async def open_supplier(
    request: Request,
    session: SessionDep,
    username: str = Depends(check_auth),
    search: str | None = None,
):
    stmt = select(Supplier)

    if search:
        stmt = stmt.where(
            or_(
                Supplier.business_name.ilike(f"%{search}%"),
                Supplier.contact_person.ilike(f"%{search}%"),
                Supplier.phone.ilike(f"%{search}%"),
            )
        )

    result = await session.execute(stmt)
    suppliers = result.scalars().all()
    return templates.TemplateResponse(
        "admin/Supplier.html",
        {
            "request": request,
            "suppliers": suppliers,
            "search": search,
        },
    )


@router.put("/supplier/{supplier_id}")
async def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    session: SessionDep,
    username: str = Depends(check_auth),
):
    supplier = await session.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(status_code=404, detail="Поставщик не найден")

    supplier.business_name = data.business_name
    supplier.contact_person = data.contact_person
    supplier.phone = data.phone

    await session.commit()
    await session.refresh(supplier)

    return {"message": "OK"}


@router.get("/price_history", name="price_history_page")
async def open_price_history(
    request: Request,
    session: SessionDep,
    username: str = Depends(check_auth),
    search: str | None = None,
):
    search_filter = None
    if search:
        search_filter = or_(
            Detail.name.ilike(f"%{search}%"),
            Detail.article.ilike(f"%{search}%"),
        )

    current_stmt = select(
        Detail.iddetails.label("detail_id"),
        Detail.name.label("name"),
        Detail.article.label("article"),
        Detail.price.label("price"),
        literal("Текущая").label("price_type"),
        literal(None, type_=Date).label("price_date"),
        literal(0, type_=Integer).label("sort_group"),
    )

    history_stmt = select(
        Detail.iddetails.label("detail_id"),
        Detail.name.label("name"),
        Detail.article.label("article"),
        History_price.price.label("price"),
        literal("Прошлая").label("price_type"),
        History_price.date.label("price_date"),
        literal(1, type_=Integer).label("sort_group"),
    ).join(
        History_price,
        History_price.detail_id == Detail.iddetails,
    )

    future_stmt = select(
        Detail.iddetails.label("detail_id"),
        Detail.name.label("name"),
        Detail.article.label("article"),
        Future_price.price.label("price"),
        literal("Будущая").label("price_type"),
        Future_price.date.label("price_date"),
        literal(2, type_=Integer).label("sort_group"),
    ).join(
        Future_price,
        Future_price.detail_id == Detail.iddetails,
    )

    if search_filter is not None:
        current_stmt = current_stmt.where(search_filter)
        history_stmt = history_stmt.where(search_filter)
        future_stmt = future_stmt.where(search_filter)

    prices_union = union_all(
        current_stmt,
        history_stmt,
        future_stmt,
    ).subquery()

    stmt = select(prices_union).order_by(
        prices_union.c.name,
        prices_union.c.article,
        prices_union.c.sort_group,
        prices_union.c.price_date.desc().nullslast(),
    )

    result = await session.execute(stmt)
    prices = result.all()

    return templates.TemplateResponse(
        "admin/Price_history.html",
        {
            "request": request,
            "prices": prices,
            "search": search,
        },
    )
