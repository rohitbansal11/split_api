from fastapi import APIRouter
from src.activity.service import create_activity, get_activity_by_id, get_all_activities, update_activity, get_activities_by_group_id, get_activities_by_user_id, delete_activity
from src.activity.scheema import ActivityCreate, Activity
from src.database.db import get_db
from src.utils.deps import get_current_user
from src.user.modal import User
from sqlalchemy.orm import Session
from fastapi import Depends
activity_router = APIRouter(
    prefix="/activity",
    tags=["activity"]
)

@activity_router.post("/create")
def create_activity_route(activity_data: ActivityCreate, db: Session = Depends(get_db)):
    activity = create_activity(db, activity_data,current_user.id)   
    return {
        "message": "Activity created successfully",
        "data": activity,
    }
@activity_router.get("/get-activity-by-id/{activity_id}")
def get_activity_by_id_route(activity_id: str, db: Session = Depends(get_db)):
    activity = get_activity_by_id(db, activity_id)
    return {
        "message": "Activity fetched successfully",
        "data": activity,
    }
@activity_router.get("/get-all-activities")
def get_all_activities_route(db: Session = Depends(get_db)):
    activities = get_all_activities(db)
    return {
        "message": "All activities fetched successfully",
        "data": activities,
    }

@activity_router.put("/update-activity/{activity_id}")
def update_activity_route(activity_id: str, activity_data: ActivityCreate, db: Session = Depends(get_db)):
    activity = update_activity(db, activity_id, activity_data)
    return {
        "message": "Activity updated successfully",
        "data": activity,
    }
@activity_router.delete("/delete-activity/{activity_id}")
def delete_activity_route(activity_id: str, db: Session = Depends(get_db)):
    activity = delete_activity(db, activity_id)
    return {
        "message": "Activity deleted successfully",
        "data": activity,
    }
@activity_router.get("/get-activities-by-group-id/{group_id}")
def get_activities_by_group_id_route(group_id: str, db: Session = Depends(get_db)):
    activities = get_activities_by_group_id(db, group_id)
    return {
        "message": "Activities fetched successfully",
        "data": activities,
    }
@activity_router.get("/get-activities-by-user-id/{user_id}")
def get_activities_by_user_id_route(user_id: str, db: Session = Depends(get_db)):
    activities = get_activities_by_user_id(db, user_id)
    return {
        "message": "Activities fetched successfully",
        "data": activities,
    }