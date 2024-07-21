from fastapi import APIRouter, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mdeposit.deposit import router

__all__ = []


class App:
    __app: FastAPI

    def __init__(self, app: FastAPI) -> None:
        self.__app = app

    def get_app(self) -> FastAPI:
        return self.__app

    def load_routers(self, routers: list[APIRouter]) -> None:
        for router in routers:
            self.__app.include_router(router)


app = App(app=FastAPI())
app.load_routers([router])
app = app.get_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": "описание ошибки"}),
    )
