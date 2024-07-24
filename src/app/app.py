import sys
from sqlalchemy import create_engine
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.app.mdeposit.deposit import deprouter
from src.app.mdeposit.depmodel import DepositModel
from src.app.conf import DBconfinit


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
    
    def setup(self):
        if "pytest" in "".join(sys.argv):
            return
        e = create_engine(DBconfinit.get_db_url_migration)
        DepositModel.metadata.create_all(bind=e)
        

app = App(app=FastAPI())
app.load_routers([deprouter])
app.setup()
app = app.get_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": "описание ошибки"}),
    )
