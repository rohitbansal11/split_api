from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.group.service import create_group, add_member_to_group, get_group_by_id, get_all_groups, get_all_members_by_group_id, get_group_calulated_expances, delete_group, delete_member_from_group
from src.group.scheema import GroupCreate, GroupMemberCreate
from src.user.modal import User
from src.utils.deps import get_current_user
from src.activity.service import create_activity
from src.activity.scheema import ActivityCreate

group_router = APIRouter(prefix="/groups", tags=["Groups"])

@group_router.post("/create-group")
def create_group_route(group_data: GroupCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    group = create_group(db, group_data,current_user.id) 
    create_activity(db, ActivityCreate(
        group_id=group.id,
        name=f"new group {group.name} created by",
        user_id=current_user.id,
    ))
    return {
        "message": "Group created successfully",
        "data": {
            "group": group,
        },
    }

@group_router.post("/add-member-to-group")
def add_member_to_group_route( member_data: GroupMemberCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    member = add_member_to_group(db, member_data) 
    create_activity(db, ActivityCreate(
        group_id=member.group_id,
        name=f"new member {member.user.name} added to group {member.group.name} by",
        user_id=current_user.id,
    ))
    return {
        "message": "Member added to group successfully",
        "data": {
            "member": member,
        },
    }

@group_router.get("/get-group-by-id/{group_id}")
def get_group_by_id_route(group_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    group = get_group_by_id(db, group_id)
    return {
        "message": "Group fetched successfully",
        "data": group,
    }

@group_router.get("/get-all-groups")
def get_all_groups_route(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    groups = get_all_groups(db ,current_user.id)
    return {
        "message": "All groups fetched successfully",
        "data": groups,
    }

@group_router.get("/get-all-members-by-group-id/{group_id}")
def get_all_members_by_group_id_route(group_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    members = get_all_members_by_group_id(db, group_id)
    return {
        "message": "All members fetched successfully",
        "data": members,
    }

@group_router.delete("/delete-group/{group_id}")
def delete_group_route(group_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    group = delete_group(db, group_id)
    create_activity(db, ActivityCreate(
        # group_id=group.id,
        name=f"group {group.name} deleted by",
        user_id=current_user.id,
    ))
    return {
        "message": "Group deleted successfully",
        "data": group,
    }
@group_router.delete("/delete-member-from-group/{group_id}/{member_id}")
def delete_member_from_group_route(group_id: str, member_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    member = delete_member_from_group(db, group_id, member_id)
    create_activity(db, ActivityCreate(
        group_id=group_id,
        name=f"member {member.user.name} deleted from group {member.group.name} by",
        user_id=current_user.id,
    ))
    return {
        "message": "Member from group deleted successfully",
        "data": member,
    }

@group_router.get("/get-group-calulated-expances/{group_id}")
def get_group_calulated_expances_route(group_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expenses = get_group_calulated_expances(db, group_id,current_user.id)
    return {
        "message": "Group calulated expances fetched successfully",
        "data": expenses,
    }













