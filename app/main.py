from typing import Union
from fastapi import FastAPI
from app.routes import user

app=FastAPI()


# @app.get("/")
# def root_func()->dict:
#     return {"hello":"world"}



app.include_router(user.router)
