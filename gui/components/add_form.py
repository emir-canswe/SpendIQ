# gui/components/add_form.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.models import Expense, CATEGORIES
from gui.styles import COLORS, FONTS, PADDING

class AddForm(tk.Frame):
    def __init__(self, parent, on_add=None, **kwargs):
        super().__init__(parent, bg=COLORS["bg_card"], **kwargs)
        self.on_add = on_add
        self._build()

    def _build(self):
        p = PADDING["section"]

        tk.Label(self, text="Yeni Harcama",
                 font=FONTS["heading"],
                 fg=COLORS["accent"],
                 bg=COLORS["bg_card"]
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=p, pady=(p, 8))

        # Başlık
        tk.Label(self, text="Başlık", font=FONTS["small"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]
        ).grid(row=1, column=0, sticky="w", padx=p)

        self._title = tk.Entry(self, font=FONTS["body"],
                               bg=COLORS["bg"], fg=COLORS["text"],
                               insertbackground=COLORS["accent"],
                               relief="flat", bd=0)
        self._title.grid(row=2, column=0, sticky="ew", padx=p, ipady=6, pady=(2, 8))

        # Tutar
        tk.Label(self, text="Tutar (₺)", font=FONTS["small"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]
        ).grid(row=1, column=1, sticky="w", padx=p)

        self._amount = tk.Entry(self, font=FONTS["amount"],
                                bg=COLORS["bg"], fg=COLORS["accent_green"],
                                insertbackground=COLORS["accent"],
                                relief="flat", bd=0)
        self._amount.grid(row=2, column=1, sticky="ew", padx=p, ipady=6, pady=(2, 8))

        # Kategori
        tk.Label(self, text="Kategori", font=FONTS["small"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]
        ).grid(row=3, column=0, sticky="w", padx=p)

        self._category = ttk.Combobox(self, values=CATEGORIES,
                                      font=FONTS["body"], state="readonly")
        self._category.set(CATEGORIES[0])
        self._category.grid(row=4, column=0, sticky="ew", padx=p, pady=(2, 8))

        # Not
        tk.Label(self, text="Not (opsiyonel)", font=FONTS["small"],
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]
        ).grid(row=3, column=1, sticky="w", padx=p)

        self._note = tk.Entry(self, font=FONTS["body"],
                              bg=COLORS["bg"], fg=COLORS["text"],
                              insertbackground=COLORS["accent"],
                              relief="flat", bd=0)
        self._note.grid(row=4, column=1, sticky="ew", padx=p, ipady=6, pady=(2, 8))

        # Ekle butonu
        tk.Button(self, text="+ Harcama Ekle",
                  font=FONTS["heading"],
                  bg=COLORS["accent"], fg=COLORS["text"],
                  activebackground=COLORS["accent"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._submit
        ).grid(row=5, column=0, columnspan=2,
               sticky="ew", padx=p, pady=(0, p), ipady=10)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _submit(self):
        title = self._title.get().strip()
        amount_str = self._amount.get().strip()
        category = self._category.get()

        if not title:
            messagebox.showerror("Hata", "Başlık boş olamaz.")
            return
        try:
            amount = float(amount_str.replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir tutar girin.")
            return

        expense = Expense.new(title, amount, category, self._note.get().strip())

        if self.on_add:
            self.on_add(expense)

        # Formu temizle
        self._title.delete(0, "end")
        self._amount.delete(0, "end")
        self._note.delete(0, "end")
        self._category.set(CATEGORIES[0])