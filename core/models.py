# core/models.py

from dataclasses import dataclass, asdict
from datetime import datetime

CATEGORIES = [
    "🍔 Yemek",
    "🚌 Ulaşım",
    "🛒 Market",
    "🎮 Eğlence",
    "💊 Sağlık",
    "📚 Eğitim",
    "🏠 Faturalar",
    "👗 Giyim",
    "📦 Diğer",
]

@dataclass
class Expense:
    id: str
    title: str
    amount: float
    category: str
    date: str  # "2026-03-14"
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Expense":
        return Expense(**data)

    @staticmethod
    def new(title: str, amount: float, category: str, note: str = "") -> "Expense":
        return Expense(
            id=datetime.now().strftime("%Y%m%d%H%M%S%f"),
            title=title,
            amount=amount,
            category=category,
            date=datetime.now().strftime("%Y-%m-%d"),
            note=note,
        )