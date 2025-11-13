from sqlalchemy.orm import Session ,joinedload
from src.expances.modal import Expense
from src.expances.scheema import ExpenseCreate ,ExpenseEdit
from fastapi import HTTPException
from sqlalchemy import or_ ,JSON
from datetime import datetime
from src.group.group_member import GroupMember
from sqlalchemy.ext.mutable import MutableDict
from src.user.modal import User

def create_expense(db:Session,expense_data:ExpenseCreate,current_user_id: str):
    try:
        group_member = db.query(GroupMember).filter(GroupMember.user_id == current_user_id,GroupMember.group_id == expense_data.group_id).first()
        if not group_member:
            raise HTTPException(status_code=404, detail="You are not a member of this group")
        
        new_expense = Expense(
            group_id=expense_data.group_id,
            name=expense_data.name,
            amount=expense_data.amount,
            group_member_id=group_member.id,
            split_between_group_member=expense_data.split_between_group_member,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_expense)

        for split in expense_data.split_between_group_member:
            group_member_to_update=db.query(GroupMember).filter(GroupMember.user_id == split["user_id"] , GroupMember.group_id == expense_data.group_id).first()
           
            if not group_member_to_update:
                raise HTTPException(status_code=404, detail="User is not a member of this group")
            found_item = next((i for i, item in enumerate(group_member_to_update.split_between_group_member)if item["user_id"] == current_user_id),None)

            if found_item is not None:
                group_member_to_update.split_between_group_member[found_item] = MutableDict(
                    group_member_to_update.split_between_group_member[found_item]
                    )
                group_member_to_update.split_between_group_member[found_item]["amount"] += split["amount"]
            else:
                group_member_to_update.split_between_group_member.append(
                    MutableDict({
                        "user_id": current_user_id,
                        "amount": split["amount"]
                    })
                )
            db.add(group_member_to_update)  # mark for update
       
        db.commit()
        db.refresh(new_expense)
        db.refresh(group_member_to_update)
        return new_expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_expenses(db:Session,group_id:str):
    try:
        expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
        updated_expenses = []
        for expense in expenses:
            user_ids= map(lambda split: split["user_id"], expense.split_between_group_member)
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            user_map = {user.id: user for user in users}

            split_with_user_details = []
            for split in expense.split_between_group_member:
                user = user_map.get(split["user_id"])
                if user:
                    split_with_user_details.append({
                        "amount": split["amount"],
                        "user_id":split["user_id"],
                        "user":user
                        })

            updated_expenses.append({
                **expense.__dict__,
                "split_between_group_member":split_with_user_details
            })
        return updated_expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def edit_expense(db:Session,expense_id:str,expense_data:ExpenseEdit,current_user_id: str):
    try:
        expense = db.query(Expense).options(joinedload(Expense.group_member)).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        
        for split in expense.split_between_group_member:
            group_member_to_update_in_reduce=db.query(GroupMember).filter(GroupMember.user_id == split["user_id"] , GroupMember.group_id == expense.group_id).first()
            found_item = next((i for i, item in enumerate(group_member_to_update_in_reduce.split_between_group_member)if item["user_id"] == expense.group_member.user_id),None)
            if found_item is not None:
                group_member_to_update_in_reduce.split_between_group_member[found_item] = MutableDict(
                    group_member_to_update_in_reduce.split_between_group_member[found_item]
                    )
                group_member_to_update_in_reduce.split_between_group_member[found_item]["amount"] -= split["amount"]
            db.add(group_member_to_update_in_reduce)  # mark for update

        expense.name = expense_data.name
        expense.amount = expense_data.amount
        expense.split_between_group_member = expense_data.split_between_group_member
        db.add(expense)  # mark for update

        for split in expense_data.split_between_group_member:
            group_member_to_update=db.query(GroupMember).filter(GroupMember.user_id == split["user_id"] , GroupMember.group_id == expense.group_id).first()
           
            if not group_member_to_update:
                raise HTTPException(status_code=404, detail="User is not a member of this group")
            found_item = next((i for i, item in enumerate(group_member_to_update.split_between_group_member)if item["user_id"] == expense.group_member.user_id),None)

            if found_item is not None:
                group_member_to_update.split_between_group_member[found_item] = MutableDict(
                    group_member_to_update.split_between_group_member[found_item]
                    )
                group_member_to_update.split_between_group_member[found_item]["amount"] += split["amount"]
            else:
                group_member_to_update.split_between_group_member.append(
                    MutableDict({
                        "user_id": expense.group_member.user_id,
                        "amount": split["amount"]
                    })
                )
            db.add(group_member_to_update)  # mark for update

        db.commit()
        db.refresh(expense)
        db.refresh(group_member_to_update)  
        return expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_expense(db:Session,expense_id:str):
    try:
        expense = db.query(Expense).options(joinedload(Expense.group_member)).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        


        for split in expense.split_between_group_member:
            group_member_to_update_in_reduce=db.query(GroupMember).filter(GroupMember.user_id == split["user_id"] , GroupMember.group_id == expense.group_id).first()
            found_item = next((i for i, item in enumerate(group_member_to_update_in_reduce.split_between_group_member)if item["user_id"] == expense.group_member.user_id),None)
            if found_item is not None:
                group_member_to_update_in_reduce.split_between_group_member[found_item] = MutableDict(
                    group_member_to_update_in_reduce.split_between_group_member[found_item]
                    )
                group_member_to_update_in_reduce.split_between_group_member[found_item]["amount"] -= split["amount"]
            db.add(group_member_to_update_in_reduce)  # mark for update


        db.delete(expense)
        db.commit()
        return expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_expense_by_id(db:Session,expense_id:str):
    try:
        expense = db.query(Expense).options(joinedload(Expense.group_member)).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        user_ids= map(lambda split: split["user_id"], expense.split_between_group_member)
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        user_map = {user.id: user for user in users}
        split_with_user_details = []
        for split in expense.split_between_group_member:
            user = user_map.get(split["user_id"])
            if user:
                split_with_user_details.append({
                    "amount": split["amount"],  
                    "user_id":split["user_id"],
                    "user":user
                })
        updated_expense = {
            **expense.__dict__,
            "split_between_group_member":split_with_user_details
        }
        return updated_expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 



























