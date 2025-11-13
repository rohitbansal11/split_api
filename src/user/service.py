from sqlalchemy.orm import Session
from src.user.modal import User
from src.user.scheema import UserCreate ,UserUpdate
from src.utils.hash import hash_password , verify_password
from fastapi import HTTPException
from sqlalchemy import or_, func

def create_user(db:Session,user_data:UserCreate):
    try:
        new_user= User(**user_data.dict())
        new_user.password = hash_password(user_data.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_user(db:Session,user_id:str,user_data:UserUpdate):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = user_data.name if user_data.name else user.name
        user.phone = user_data.phone if user_data.phone else user.phone
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_user(db:Session,user_id:str):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_by_id(db:Session,user_id:str):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_by_email(db:Session,email:str):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_users(db:Session):
    try:
        users = db.query(User).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def user_exists(db:Session,email:str):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def authenticate_user(db:Session,email:str,password:str):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password,user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def search_user_by_email_name_phone(db: Session, value: str,current_user_id: str):
    try:
        value_lower = value.lower()
        users = db.query(User).filter(
            or_(
                func.lower(User.email).like(f"%{value_lower}%"),
                func.lower(User.name).like(f"%{value_lower}%"),
                func.lower(User.phone).like(f"%{value_lower}%")
            )
        ).filter(User.id != current_user_id).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









