from fastapi import APIRouter ,Depends ,status, HTTPException
from src.connect import service as connectService
from src.connect.scheema import ConnectCreate
from src.database.db import SessionLocal ,get_db
from sqlalchemy.orm import Session
from src.utils.deps import get_current_user
from src.user.modal import User

connect_router = APIRouter(prefix="/connects", tags=["Connects"])

@connect_router.post('/',status_code=status.HTTP_201_CREATED)
def create_connect(connect_data:ConnectCreate,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    connect= connectService.create_connect(db,connect_data,current_user.id)
    return {
        "message": "Connect created successfully",
        "data": {
            "connect": connect,
        },
    }

@connect_router.get('/',status_code=status.HTTP_200_OK)
def get_all_connects(db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    connects= connectService.get_all_connects(db,current_user.id)
    return {
        "message": "Connects fetched successfully",
        "data": {
            "connects": connects,
        },
    }

@connect_router.get('/{connect_id}',status_code=status.HTTP_200_OK)
def get_connect_by_id(connect_id:str,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    connect= connectService.get_connect_by_id(db,connect_id)
    return {
        "message": "Connect fetched successfully",
        "data": {
            "connect": connect,
        },
    }

@connect_router.delete('/{connect_id}',status_code=status.HTTP_200_OK)
def delete_connect(connect_id:str,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    connect= connectService.delete_connect(db,connect_id)
    return {
        "message": "Connect deleted successfully",
        "data": {
            "connect": connect,
        },
    }