# core/storage.py

import json
from pathlib import Path
from core.models import Expense

DATA_FILE = Path("data/expenses.json")

def _ensure_file():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists() or DATA_FILE.read_text(encoding="utf-8").strip() == "":
        DATA_FILE.write_text(
            json.dumps({"expenses": [], "budget": 0}, indent=2),
            encoding="utf-8"
        )

def load_all() -> list[Expense]:
    _ensure_file()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Expense.from_dict(e) for e in data["expenses"]]

def save_all(expenses: list[Expense]):
    _ensure_file()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data["expenses"] = [e.to_dict() for e in expenses]
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def add_expense(expense: Expense):
    expenses = load_all()
    expenses.append(expense)
    save_all(expenses)

def delete_expense(expense_id: str):
    expenses = load_all()
    expenses = [e for e in expenses if e.id != expense_id]
    save_all(expenses)

def get_budget() -> float:
    _ensure_file()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return float(data.get("budget", 0))

def set_budget(amount: float):
    _ensure_file()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data["budget"] = amount
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )