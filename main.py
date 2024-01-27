from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from hashlib import sha256
import databases
import sqlalchemy
from sqlalchemy import ForeignKey

DATABASE_URL = "sqlite:///my_shop.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("users.id")),
    sqlalchemy.Column("good_id", sqlalchemy.Integer, ForeignKey("goods.id")),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(32)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

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
    date: datetime = Field(default=datetime.now())
    status: bool = Field(default=False)


class OrderIn(BaseModel):
    user_id: int
    good_id: int
    date: datetime = Field(default=datetime.now())
    status: bool = Field(default=False)


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
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# CRUD for users
@app.post("/fake_users/{count}")
async def create_user(count: int):
    for i in range(count):
        query = users.insert().values(first_name=f'user{i}', surname=f"user_{i}_surname", email=f'mail{i}@mail.ru',
                                      password=sha256(f'{i}_user_password'.encode(encoding='utf-8')).hexdigest())
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.post("/fake_goods/{count}")
async def create_good(count: int):
    for i in range(count):
        query = goods.insert().values(name=f'user{i}', description=f'good_{i}description', price=f"100{i}")
        await database.execute(query)
    return {'message': f'{count} fake goods created'}


@app.post("/fake_orders/{count}")
async def create_order(count: int):
    for i in range(count):
        query = orders.insert().values(user_id=f'{i}', good_id=f'{i}', date=datetime.now(), status=False)
        await database.execute(query)
    return {'message': f'{count} fake orders created'}


# CRUD for users
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# CRUD for goods
@app.post("/goods/", response_model=Good)
async def create_good(good: GoodIn):
    query = goods.insert().values(**good.model_dump())
    last_record_id = await database.execute(query)
    return {**good.model_dump(), "id": last_record_id}


@app.get("/goods/", response_model=List[Good])
async def read_good():
    query = goods.select()
    return await database.fetch_all(query)


@app.get("goods/{good_id}", response_model=Good)
async def read_good(good_id: int):
    query = goods.select().where(goods.c.id == good_id)
    return await database.fetch_one(query)


@app.put("goods/{good_id}", response_model=Good)
async def update_good(good_id: int, new_good: GoodIn):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.model_dump())
    await database.execute(query)
    return {**new_good.model_dump(), "id": good_id}


@app.delete("/goods/{good_id}")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    await database.execute(query)
    return {'message': 'Good deleted'}


# CRUD for orders
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
