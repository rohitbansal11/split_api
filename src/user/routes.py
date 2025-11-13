from fastapi import APIRouter ,Depends ,status, HTTPException
from src.user import service as userService
from src.user.scheema import UserCreate, LoginRequest, UserUpdate
from src.database.db import SessionLocal ,get_db
from sqlalchemy.orm import Session
from src.utils.deps import get_current_user
from src.utils.jwt_handler import create_access_token
from src.user.modal import User

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(user_data:UserCreate,db:Session=Depends(get_db)):
    user= userService.create_user(db,user_data)
    return {
        "message": "User created successfully",
        "data": {
            "user": user,
        },
    }

@user_router.put('/{user_id}',status_code=status.HTTP_200_OK)
def update_user(user_id:str,user_data:UserUpdate,db:Session=Depends(get_db)):
    user= userService.update_user(db,user_id,user_data)
    return {
        "message": "User updated successfully",
        "data": {
            "user": user,
        },
    }

@user_router.delete('/{user_id}',status_code=status.HTTP_200_OK)
def delete_user(user_id:str,db:Session=Depends(get_db)):
    user= userService.delete_user(db,user_id)
    return {
        "message": "User deleted successfully",
        "data": {
            "user": user,
        },
    }

@user_router.get('/{user_id}',status_code=status.HTTP_200_OK)
def get_user(user_id:str,db:Session=Depends(get_db)):
    user= userService.get_user_by_id(db,user_id)
    return {
        "message": "User fetched successfully",
        "data": {
            "user": user,
        },
    }

@user_router.get('/',status_code=status.HTTP_200_OK)
def get_all_users(db:Session=Depends(get_db)):
    users= userService.get_all_users(db)
    return {
        "message": "Users fetched successfully",
        "data": {
            "users": users,
        },
    }

@user_router.get('/email/{email}',status_code=status.HTTP_200_OK)
def get_user_by_email(email:str,db:Session=Depends(get_db)):
    user= userService.get_user_by_email(db,email)
    return {
        "message": "User fetched successfully",
        "data": {
            "user": user,
        },
    }

@user_router.get('/exists/{email}',status_code=status.HTTP_200_OK)
def user_exists(email:str,db:Session=Depends(get_db)):
    exists= userService.user_exists(db,email)
    return {
        "message": "User exists",
        "data": {
            "exists": exists,
        },
    }

@user_router.post('/login',status_code=status.HTTP_200_OK)
def login_user(login_data:LoginRequest,db:Session=Depends(get_db)):
    user= userService.authenticate_user(db,login_data.email,login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    token = create_access_token({
        "email": user.email,
        "user_id": user.id,
    })
    return {
        "message": "Login successful",
        "data": {
            "access_token": token,
            "token_type": "Bearer",
            "user": user,
        },
    }

@user_router.get('/checkuser/me',status_code=status.HTTP_200_OK)
def get_current_user_routes(db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    return {
        "message": "Current user fetched successfully",
        "data": {
            "user": current_user,
        },
    }


@user_router.get('/search/{value}',status_code=status.HTTP_200_OK)
def search_user(value:str,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
   
    users= userService.search_user_by_email_name_phone(db,value,current_user.id)
    return {
        "message": "Users fetched successfully",
        "data": {
            "users": users,
        },
    }