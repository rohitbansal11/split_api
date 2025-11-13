from sqlalchemy.orm import Session ,joinedload
from src.group.group_modal import Group
from src.group.group_member import GroupMember
from src.group.scheema import GroupCreate, GroupMemberCreate
from fastapi import HTTPException
from sqlalchemy import or_
from datetime import datetime
from src.user.modal import User
from src.expances.modal import Expense

def create_group(db:Session,group_data:GroupCreate,current_user_id: str):
    try:
        new_group = Group(
            name=group_data.name,
            type=group_data.type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        new_member = add_member_to_group(db, GroupMemberCreate(group_id=new_group.id, user_id=current_user_id))
        return new_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_member_to_group(db:Session,member_data:GroupMemberCreate):
    try:
        member_exists = db.query(GroupMember).filter(GroupMember.group_id == member_data.group_id, GroupMember.user_id == member_data.user_id).first()
        if member_exists:
            raise HTTPException(status_code=400, detail="Member already exists")

        new_member = GroupMember(
            group_id=member_data.group_id,
            user_id=member_data.user_id,
        )
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

def get_group_by_id(db:Session,group_id: str):
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_groups(db:Session,current_user_id: str):
    try:
        groups = db.query(Group).options(joinedload(Group.members)).join(GroupMember).filter(GroupMember.user_id == current_user_id).all()
        return groups
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_members_by_group_id(db:Session,group_id: str):
    try:
        members = (
            db.query(GroupMember)
            .options(joinedload(GroupMember.user))  
            .filter(GroupMember.group_id == group_id)
            .all()
        )
        updated_members = []
        for member in members:
            user_ids= map(lambda split: split["user_id"], member.split_between_group_member)
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            user_map = {user.id: user for user in users}

            split_with_user_details = []
            for split in member.split_between_group_member:
                user = user_map.get(split["user_id"])
                if user:
                    split_with_user_details.append({
                        "amount": split["amount"],
                        "user_id":split["user_id"],
                        "user":user
                        })

            updated_members.append({
                **member.__dict__,
                "split_between_group_member":split_with_user_details
            })


        return updated_members
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_group(db:Session,group_id: str):
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        db.delete(group)
        db.refresh(group)
        db.commit()
        return group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_member_from_group(db:Session,group_id: str,member_id: str):
    try:
        member_from_group = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == member_id).first()
        if not member_from_group:
            raise HTTPException(status_code=404, detail="Member from group not found")
        db.delete(member_from_group)
        db.commit() 
        db.refresh(member_from_group)   # ✅ refresh to get updated instance
        return member_from_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_group_calulated_expances(db:Session,group_id: str,current_user_id: str):
    try:
        group_member = get_all_members_by_group_id(db,group_id)
        getCurrentUser = next((member for member in group_member if member["user_id"] == current_user_id),None)
        otherMembers = filter(lambda member: member["user_id"] != current_user_id, group_member)

        final_result = []
        for otherMember in list(otherMembers):

            otherMemberUser = otherMember['user'].__dict__

            expancesUserHasToPay = next((member for member in otherMember['split_between_group_member'] if member["user_id"] == current_user_id),None)

            expancesOtherUserHasToPay = next((member for member in getCurrentUser['split_between_group_member'] if member["user_id"] == otherMember["user_id"]),None)


            if expancesUserHasToPay and expancesOtherUserHasToPay:
                if expancesUserHasToPay["amount"] > expancesOtherUserHasToPay["amount"]:
                    final_result.append({
                        "user_id":otherMember["user_id"],
                        "amount":expancesUserHasToPay["amount"] - expancesOtherUserHasToPay["amount"],
                        "name":otherMemberUser["name"],
                        "email":otherMemberUser["email"],
                    })
                elif expancesUserHasToPay["amount"] < expancesOtherUserHasToPay["amount"]:
                    final_result.append({
                        "user_id":otherMember["user_id"],
                        "amount":expancesOtherUserHasToPay["amount"] - expancesUserHasToPay["amount"],
                        "name":otherMemberUser["name"],
                        "email":otherMemberUser["email"],
                    })
                else:
                    final_result.append({
                        "user_id":otherMember["user_id"],
                        "amount":0,
                        "name":otherMemberUser["name"],
                        "email":otherMemberUser["email"],
                        })

        return final_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))















