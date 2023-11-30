from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get("/")
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operation).where(
            operation.c.type == operation_type
        )  # str(query) for debugging
        result = await session.execute(query)
        return result.mappings().all()
    except (ZeroDivisionError, Exception) as e:
        return HTTPException(
            status_code=500,
            detail={"status": "error", "data": None, "details": "Zero division error"}
            if isinstance(e, ZeroDivisionError)
            else {"status": "error", "data": None, "details": "Something went wrong"},
        )



@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
