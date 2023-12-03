import os

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operations.router import get_specific_operations


def create_frontend_router(base_directory: str):
    router = APIRouter(
        prefix="/pages",
        tags=["Pages"]
    )

    templates = Jinja2Templates(directory=os.path.join(base_directory, "frontend/templates"))
    router.get("/base")

    @router.get("/base")
    def get_base_page(request: Request):
        return templates.TemplateResponse("base.html", {"request": request})

    @router.get("/search/{operation_type}")
    def get_search_page(request: Request, operations=Depends(get_specific_operations)):
        return templates.TemplateResponse("search.html", {"request": request, "operations": operations})

    @router.get("/chat")
    def get_chat_page(request: Request):
        return templates.TemplateResponse("chat.html", {"request": request})

    return router
