# core/budget.py

from datetime import datetime
from core.models import Expense

def get_monthly_expenses(expenses: list[Expense], year: int = None, month: int = None) -> list[Expense]:
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    return [
        e for e in expenses
        if e.date.startswith(f"{year}-{month:02d}")
    ]

def get_total(expenses: list[Expense]) -> float:
    return sum(e.amount for e in expenses)

def get_by_category(expenses: list[Expense]) -> dict[str, float]:
    result = {}
    for e in expenses:
        result[e.category] = result.get(e.category, 0) + e.amount
    return result

def get_budget_status(expenses: list[Expense], budget: float) -> dict:
    monthly = get_monthly_expenses(expenses)
    spent = get_total(monthly)
    remaining = budget - spent
    percent = (spent / budget * 100) if budget > 0 else 0

    return {
        "spent": spent,
        "budget": budget,
        "remaining": remaining,
        "percent": min(percent, 100),
        "over_budget": spent > budget and budget > 0,
        "warning": percent >= 80 and budget > 0,
    }