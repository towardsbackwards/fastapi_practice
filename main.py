from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title='Testing App'
)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


fake_users = [
    {"id": 1, "role": "admin", "name": ["Bob"],
     "degree": [{"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}]},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def hello(user_id: int):
    resp = [u for u in fake_users if u.get("id") == user_id]
    if resp:
        return resp[0]
    return {"data": 'User not found'}


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "buy", "price": 125, "amount": 2.12},
]


@app.get("/trades")
def get_trades(limit: int = 10, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users_2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]


@app.post("/users/{user_id}")
def change_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users_2))
    if current_user:
        current_user[0]['name'] = new_name
        return {"status": 200, "data": current_user[0]}
    return 'User not found'


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
