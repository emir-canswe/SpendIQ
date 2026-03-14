# gui/app.py

import tkinter as tk
from core import storage
from core.budget import get_monthly_expenses, get_total, get_budget_status
from gui.styles import COLORS, FONTS, PADDING
from gui.components.add_form import AddForm
from gui.components.expense_list import ExpenseList
from gui.components.chart_panel import ChartPanel
from gui.components.budget_bar import BudgetBar

class SpendIQApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SpendIQ")
        self.geometry("900x620")
        self.resizable(True, True)
        self.configure(bg=COLORS["bg"])
        self._build()
        self._refresh()

    def _build(self):
        p = PADDING["window"]

        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=p, pady=(18, 0))

        tk.Label(header, text="💰 SpendIQ",
                 font=FONTS["title"],
                 fg=COLORS["accent"],
                 bg=COLORS["bg"]
        ).pack(side="left")

        self._total_lbl = tk.Label(header, text="",
                                   font=FONTS["amount"],
                                   fg=COLORS["accent_red"],
                                   bg=COLORS["bg"])
        self._total_lbl.pack(side="right")

        tk.Frame(self, bg=COLORS["border"], height=1).pack(
            fill="x", padx=p, pady=10)

        self._budget_bar = BudgetBar(self, on_budget_set=self._on_budget_set)
        self._budget_bar.pack(fill="x", padx=p, pady=(0, 10))

        tk.Frame(self, bg=COLORS["border"], height=1).pack(
            fill="x", padx=p, pady=(0, 10))

        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=p)

        left = tk.Frame(content, bg=COLORS["bg"])
        left.pack(side="left", fill="both", expand=True)

        self._form = AddForm(left, on_add=self._on_add)
        self._form.pack(fill="x", pady=(0, 10))

        self._list = ExpenseList(left, on_delete=self._on_delete)
        self._list.pack(fill="both", expand=True)

        right = tk.Frame(content, bg=COLORS["bg"])
        right.pack(side="right", fill="both", padx=(16, 0))

        self._chart = ChartPanel(right)
        self._chart.pack(fill="both", expand=True)

    def _refresh(self):
        expenses = storage.load_all()
        budget   = storage.get_budget()
        monthly  = get_monthly_expenses(expenses)
        total    = get_total(monthly)
        status   = get_budget_status(expenses, budget)

        self._total_lbl.configure(text=f"Bu ay: ₺{total:,.2f}")
        self._list.refresh(expenses)
        self._chart.refresh(monthly)
        self._budget_bar.refresh(status)

        if status["over_budget"]:
            self.configure(bg="#1a0a0a")
        else:
            self.configure(bg=COLORS["bg"])

    def _on_add(self, expense):
        storage.add_expense(expense)
        self._refresh()

    def _on_delete(self, expense_id):
        storage.delete_expense(expense_id)
        self._refresh()

    def _on_budget_set(self, amount):
        storage.set_budget(amount)
        self._refresh()

    def on_closing(self):
        self.destroy()