# gui/components/expense_list.py

import tkinter as tk
from tkinter import ttk
from core.models import Expense
from gui.styles import COLORS, FONTS

class ExpenseList(tk.Frame):
    def __init__(self, parent, on_delete=None, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self.on_delete = on_delete
        self._build()

    def _build(self):
        tk.Label(self, text="Harcamalar",
                 font=FONTS["heading"],
                 fg=COLORS["accent"],
                 bg=COLORS["bg"]
        ).pack(anchor="w", pady=(0, 6))

        # Tablo
        columns = ("date", "title", "category", "amount")
        self._tree = ttk.Treeview(self, columns=columns,
                                  show="headings", height=10)

        self._tree.heading("date",     text="Tarih")
        self._tree.heading("title",    text="Başlık")
        self._tree.heading("category", text="Kategori")
        self._tree.heading("amount",   text="Tutar")

        self._tree.column("date",     width=90,  anchor="center")
        self._tree.column("title",    width=160, anchor="w")
        self._tree.column("category", width=120, anchor="center")
        self._tree.column("amount",   width=90,  anchor="e")

        scrollbar = ttk.Scrollbar(self, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sil butonu
        tk.Button(self, text="🗑 Seçili Sil",
                  font=FONTS["small"],
                  bg=COLORS["bg_card"], fg=COLORS["accent_red"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._delete_selected
        ).pack(anchor="e", pady=(6, 0))

        # Seçili satırın ID'sini sakla
        self._id_map = {}

    def refresh(self, expenses: list):
        self._tree.delete(*self._tree.get_children())
        self._id_map.clear()

        for e in sorted(expenses, key=lambda x: x.date, reverse=True):
            row_id = self._tree.insert("", "end", values=(
                e.date,
                e.title,
                e.category,
                f"₺{e.amount:,.2f}"
            ))
            self._id_map[row_id] = e.id

    def _delete_selected(self):
        selected = self._tree.selection()
        if not selected:
            return
        for row_id in selected:
            expense_id = self._id_map.get(row_id)
            if expense_id and self.on_delete:
                self.on_delete(expense_id)