from sqlalchemy.orm import Session
from src.activity.modal import Activity
from src.activity.scheema import ActivityCreate

def create_activity(db:Session,activity_data:ActivityCreate):
    new_activity = Activity(
        group_id=activity_data.group_id,
        name=activity_data.name,
        user_id=activity_data.user_id,
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

def get_activity_by_id(db:Session,activity_id:str):
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_all_activities(db:Session):
    return db.query(Activity).all()

def update_activity(db:Session,activity_id:str,activity_data:ActivityCreate):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    activity.name = activity_data.name
    activity.user_id = activity_data.user_id
    db.commit()
    db.refresh(activity)


def get_activities_by_group_id(db:Session,group_id:str):
    return db.query(Activity).filter(Activity.group_id == group_id).all()

def get_activities_by_user_id(db:Session,user_id:str):
    return db.query(Activity).filter(Activity.user_id == user_id).all()

def delete_activity(db:Session,activity_id:str):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    db.delete(activity)
    db.commit()
    return activity