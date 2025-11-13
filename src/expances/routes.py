from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.expances.scheema import ExpenseCreate, ExpenseEdit
from src.expances.service import create_expense, edit_expense, delete_expense, get_expenses, get_expense_by_id
from src.database.db import get_db
from src.utils.deps import get_current_user
from src.user.modal import User


expense_router = APIRouter(
    prefix="/expances",
    tags=["expances"]
)

@expense_router.post("/create-expense") 
def create_expense_route(expense_data: ExpenseCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = create_expense(db, expense_data,current_user.id)
    return {
        "message": "Expense created successfully",
        "data": expense,
    }

@expense_router.put("/edit-expense/{expense_id}")
def edit_expense_route(expense_id: str, expense_data: ExpenseEdit, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = edit_expense(db, expense_id, expense_data,current_user.id)
    return {
        "message": "Expense edited successfully",
        "data": expense,
    }

@expense_router.delete("/delete-expense/{expense_id}")
def delete_expense_route(expense_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = delete_expense(db, expense_id)
    return {
        "message": "Expense deleted successfully",
        "data": expense,
    }

@expense_router.get("/get-expenses/{group_id}")
def get_expenses_route(group_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expenses = get_expenses(db, group_id)
    return {
        "message": "Expenses fetched successfully",
        "data": expenses,
    }
@expense_router.get("/get-expense-by-id/{expense_id}")
def get_expense_by_id_route(expense_id: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = get_expense_by_id(db, expense_id)
    return {
        "message": "Expense fetched successfully",
        "data": expense,
    }

