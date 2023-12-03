import time

import redis.asyncio as aioredis  # it's OK
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate
from chat.router import router as router_chat
from config import REDIS_HOST, REDIS_PORT
from frontend.pages.router import router as router_frontend
from operations.router import router as router_operation
from tasks.routers import router as router_tasks

app = FastAPI(
    title='Testing App'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route():
    return "Hello, anonymous user!"


@app.get("/cached-route")
@cache(expire=300)
def protected_route():
    time.sleep(2)
    return "This page is cached"


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_frontend)
app.include_router(router_chat)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
