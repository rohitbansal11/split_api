from sqlalchemy.orm import Session
from src.connect.modal import Connect
from src.connect.scheema import ConnectCreate
from fastapi import HTTPException
from sqlalchemy import or_

def create_connect(db:Session,connect_data:ConnectCreate,current_user_id: str):
  
    try:
        connect_exists = db.query(Connect).filter(
            or_(
                (Connect.user_id_one == connect_data.user_id_two) & (Connect.user_id_two == current_user_id),
                (Connect.user_id_two == connect_data.user_id_two) & (Connect.user_id_one == current_user_id)
                )
                ).first()

        if connect_exists:
            raise HTTPException(status_code=400, detail="Connect already exists")

        new_connect= Connect(
            user_id_one=current_user_id,
            user_id_two=connect_data.user_id_two,
            device_name=connect_data.device_name or "Unknown Device"
        )
        db.add(new_connect)
        db.commit()
        db.refresh(new_connect)
        return new_connect
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_all_connects(db:Session,current_user_id: str):
    try:
        connects = db.query(Connect).filter(
            or_(
                Connect.user_id_one == current_user_id,
                Connect.user_id_two == current_user_id
                )
                ).all()
        return connects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_connect_by_id(db:Session,connect_id: str):
    try:
        connect = db.query(Connect).filter(Connect.id == connect_id).first()
        return connect
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_connect(db:Session,connect_id: str):
    try:
        connect = db.query(Connect).filter(Connect.id == connect_id).first()
        if not connect:
            raise HTTPException(status_code=404, detail="Connect not found")
        db.delete(connect)
        db.commit()
        return connect
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))