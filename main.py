from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request
import logging
from hashlib import sha256
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates
import databases
import sqlalchemy
from sqlalchemy import ForeignKey

DATABASE_URL = "sqlite:///shop.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Integer)
    #ForeignKey("name", _constraint="orders.id")
)


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("good_id", sqlalchemy.Integer),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.Boolean)
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(32)),
    sqlalchemy.Column("password", sqlalchemy.String(32))
)


engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    first_name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=32)
    password: str = Field(max_length=16)


class UserIn(BaseModel):
    first_name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=32)
    password: str = Field(max_length=16)

class Order(BaseModel):
    id: int
    user_id: int
    good_id: int
    date: datetime
    status: bool


class OrderIn(BaseModel):
    user_id: int
    good_id: int
    date: datetime
    status: bool

class Good(BaseModel):
    id: int
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float


class GoodIn(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float
@app.on_event("startup")
async def starup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()