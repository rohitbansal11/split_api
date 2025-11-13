from fastapi import FastAPI
from src.database.db import engine, Base
from src.connect.routes import connect_router

    #  Middleware

from src.utils.errors import register_all_errors
from src.utils.middleware import register_middleware

    #  Db Models
from src.user.modal import User
from src.connect.modal import Connect
from src.group.group_modal import Group
from src.group.group_member import GroupMember
from src.expances.modal import Expense
from src.activity.modal import Activity

    #  Routes
from src.user.routes import user_router
from src.connect.routes import connect_router
from src.group.routes import group_router
from src.expances.routes import expense_router



app = FastAPI()


app.include_router(user_router)
app.include_router(connect_router)
app.include_router(group_router)
app.include_router(expense_router)


# Create database tables
Base.metadata.create_all(bind=engine)

register_all_errors(app)

register_middleware(app)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}