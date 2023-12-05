import json
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from pydantic import BaseModel
from sqlalchemy import select


class AdditionalInfo(BaseModel):
    divorced: bool


class TestUser(BaseModel):
    name: str
    last_name: str
    age: int
    additional_info: dict


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def redis_cache(ttl: int):
    def wrapper(call: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:

        @wraps(call)
        async def inner(self, *args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            if not args:
                return  # or Raise
            cas_id = args[0]
            cache_key = f'tinder_has_user_{cas_id}'
            cache_data = await self._redis.get(cache_key)
            if cache_data:
                return json.loads(cache_data)
            else:
                result = await call(self, *args, **kwargs)
                await self._redis.set(cache_key, json.dumps(result), ttl)
                return result

        return inner

    return wrapper


class CasRepository:
    def __init__(self, redis, session):
        self._redis = redis
        self._session = session

    @redis_cache(ttl=15)
    async def get_operation_by_id(self, operation_id: int) -> dict:
        from operations.models import operation
        query = select(operation).filter(operation.c.id == operation_id)
        result = await self._session.execute(query)
        row = result.first()
        if not row:
            return {}

        # Convert Row to dictionary
        result_dict = {k: v for k, v in zip(range(6), row)}

        return result_dict
