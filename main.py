# main.py

from gui.app import SpendIQApp

if __name__ == "__main__":
    app = SpendIQApp()
    app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()