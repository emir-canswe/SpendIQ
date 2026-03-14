# gui/components/budget_bar.py

import tkinter as tk
from gui.styles import COLORS, FONTS

class BudgetBar(tk.Frame):
    def __init__(self, parent, on_budget_set=None, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self.on_budget_set = on_budget_set
        self._build()

    def _build(self):
        # Üst satır: başlık + limit ayarı
        top = tk.Frame(self, bg=COLORS["bg"])
        top.pack(fill="x", pady=(0, 4))

        tk.Label(top, text="Aylık Bütçe",
                 font=FONTS["heading"],
                 fg=COLORS["accent"],
                 bg=COLORS["bg"]
        ).pack(side="left")

        self._budget_entry = tk.Entry(top, width=10,
                                      font=FONTS["body"],
                                      bg=COLORS["bg_card"],
                                      fg=COLORS["text"],
                                      insertbackground=COLORS["accent"],
                                      relief="flat", bd=0)
        self._budget_entry.pack(side="right", ipady=4, ipadx=6)

        tk.Button(top, text="Kaydet",
                  font=FONTS["small"],
                  bg=COLORS["accent"], fg=COLORS["text"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._save_budget
        ).pack(side="right", padx=(0, 4), ipady=4, ipadx=8)

        tk.Label(top, text="Limit (₺):",
                 font=FONTS["small"],
                 fg=COLORS["text_muted"],
                 bg=COLORS["bg"]
        ).pack(side="right", padx=(0, 4))

        # Durum yazısı
        self._status_lbl = tk.Label(self,
                                    text="Bütçe ayarlanmadı",
                                    font=FONTS["small"],
                                    fg=COLORS["text_muted"],
                                    bg=COLORS["bg"])
        self._status_lbl.pack(anchor="w", pady=(0, 4))

        # Progress bar canvas
        self._canvas = tk.Canvas(self, height=16,
                                 bg=COLORS["bg_card"],
                                 highlightthickness=0)
        self._canvas.pack(fill="x")

    def _save_budget(self):
        val = self._budget_entry.get().strip()
        try:
            amount = float(val.replace(",", "."))
            if self.on_budget_set:
                self.on_budget_set(amount)
        except ValueError:
            pass

    def refresh(self, status: dict):
        self._canvas.delete("all")
        width = self._canvas.winfo_width() or 400

        spent   = status["spent"]
        budget  = status["budget"]
        percent = status["percent"]

        # Renk seç
        if status["over_budget"]:
            color = COLORS["accent_red"]
        elif status["warning"]:
            color = COLORS["accent_warn"]
        else:
            color = COLORS["accent_green"]

        # Bar çiz
        fill_width = int(width * percent / 100)
        self._canvas.create_rectangle(0, 0, fill_width, 16,
                                      fill=color, outline="")

        # Durum yazısı
        if budget <= 0:
            msg = "Bütçe ayarlanmadı"
            fg = COLORS["text_muted"]
        elif status["over_budget"]:
            msg = f"⚠ Bütçe aşıldı!  ₺{spent:,.0f} / ₺{budget:,.0f}"
            fg = COLORS["accent_red"]
        elif status["warning"]:
            msg = f"⚡ Bütçenin %{percent:.0f}'i harcandı  ₺{spent:,.0f} / ₺{budget:,.0f}"
            fg = COLORS["accent_warn"]
        else:
            msg = f"✓ ₺{spent:,.0f} harcandı  /  ₺{budget - spent:,.0f} kaldı"
            fg = COLORS["accent_green"]

        self._status_lbl.configure(text=msg, fg=fg)