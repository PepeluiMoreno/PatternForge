from typing import Any, Dict, List, Optional
from ariadne import ObjectType
from sqlalchemy import select

def _touch_timestamps(obj):
    import datetime
    now = datetime.datetime.utcnow()
    if hasattr(obj, "updated_at"):
        setattr(obj, "updated_at", now)
    if hasattr(obj, "created_at") and getattr(obj, "created_at", None) is None:
        setattr(obj, "created_at", now)

def build_crud_resolvers(
    type_name: str,
    model,
    list_field: str,
    single_field: str,
    create_field: str,
    update_field: str,
    delete_field: str,
    searchable_cols: Optional[List] = None,
    unique_checks: Optional[List] = None,
):
    query = ObjectType("Query")
    mutation = ObjectType("Mutation")
    node = ObjectType(type_name)
    searchable_cols = searchable_cols or []
    unique_checks = unique_checks or []

    @query.field(list_field)
    async def resolve_list(*_, search: Optional[str] = None, offset: int = 0, limit: int = 50, orderBy: Optional[str] = None, order: str = "ASC"):
        session = _[1].context["session"]
        stmt = select(model)
        if search and searchable_cols:
            from sqlalchemy import or_
            ors = [col.ilike(f"%{search}%") for col in searchable_cols]
            stmt = stmt.where(or_(*ors))
        if orderBy:
            col = getattr(model, orderBy, None)
            if col is not None:
                stmt = stmt.order_by(col.asc() if order.upper()=="ASC" else col.desc())
        stmt = stmt.offset(offset).limit(limit)
        res = await session.execute(stmt)
        return res.scalars().all()

    @query.field(single_field)
    async def resolve_single(*_, id: str):
        session = _[1].context["session"]
        res = await session.execute(select(model).where(model.id == id))
        return res.scalar_one_or_none()

    async def _check_uniques(session, input: Dict[str, Any], ignore_id: Optional[str] = None):
        if not unique_checks:
            return
        from sqlalchemy import and_
        for col in unique_checks:
            if col.key in input:
                value = input[col.key]
                stmt = select(model).where(col == value)
                if ignore_id is not None:
                    stmt = stmt.where(model.id != ignore_id)
                exists = (await session.execute(stmt)).scalar_one_or_none()
                if exists:
                    raise ValueError(f"Unique constraint violated for field '{col.key}'")

    @mutation.field(create_field)
    async def resolve_create(*_, input: Dict[str, Any]):
        session = _[1].context["session"]
        await _check_uniques(session, input)
        obj = model(**input)
        _touch_timestamps(obj)
        session.add(obj)
        await session.flush()
        return obj

    @mutation.field(update_field)
    async def resolve_update(*_, id: str, input: Dict[str, Any]):
        session = _[1].context["session"]
        res = await session.execute(select(model).where(model.id == id))
        obj = res.scalar_one_or_none()
        if not obj:
            return None
        await _check_uniques(session, input, ignore_id=id)
        for k, v in input.items():
            setattr(obj, k, v)
        _touch_timestamps(obj)
        await session.flush()
        return obj

    @mutation.field(delete_field)
    async def resolve_delete(*_, id: str):
        session = _[1].context["session"]
        res = await session.execute(select(model).where(model.id == id))
        obj = res.scalar_one_or_none()
        if not obj:
            return False
        await session.delete(obj)
        return True

    return query, mutation, node
