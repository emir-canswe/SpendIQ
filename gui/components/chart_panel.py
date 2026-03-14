# gui/components/chart_panel.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.budget import get_by_category
from gui.styles import COLORS, FONTS

CHART_COLORS = [
    "#6366f1", "#10b981", "#f59e0b", "#ef4444",
    "#8b5cf6", "#06b6d4", "#f97316", "#84cc16"
]

class ChartPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self._build()

    def _build(self):
        tk.Label(self, text="Kategori Dağılımı",
                 font=FONTS["heading"],
                 fg=COLORS["accent"],
                 bg=COLORS["bg"]
        ).pack(anchor="w", pady=(0, 6))

        self._fig = Figure(figsize=(4, 3), dpi=90)
        self._fig.patch.set_facecolor(COLORS["bg"])

        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor(COLORS["bg_card"])

        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh(self, expenses: list):
        self._ax.clear()
        self._ax.set_facecolor(COLORS["bg_card"])

        by_cat = get_by_category(expenses)

        if not by_cat:
            self._ax.text(0.5, 0.5, "Henüz harcama yok",
                          ha="center", va="center",
                          color=COLORS["text_muted"],
                          fontsize=10,
                          transform=self._ax.transAxes)
            self._canvas.draw()
            return

        labels = list(by_cat.keys())
        values = list(by_cat.values())
        colors = CHART_COLORS[:len(labels)]

        wedges, texts, autotexts = self._ax.pie(
            values,
            labels=None,
            colors=colors,
            autopct="%1.0f%%",
            startangle=90,
            pctdistance=0.75,
        )

        for t in autotexts:
            t.set_color(COLORS["text"])
            t.set_fontsize(8)

        self._ax.legend(
            wedges, labels,
            loc="lower center",
            ncol=2,
            fontsize=7,
            facecolor=COLORS["bg_card"],
            labelcolor=COLORS["text"],
            framealpha=0.5,
        )

        self._canvas.draw()