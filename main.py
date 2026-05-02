"""
main.py — Entry point FinTrack Mini
Hanya inisialisasi app, load style, tampilkan window.
"""
import sys
import os

# Pastikan root project selalu masuk ke sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from database.db_manager import init_db    # tambah import ini
from ui.main_window import MainWindow


def load_style(app):
    qss_path = os.path.join(BASE_DIR, "style", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    load_style(app)

    init_db()              # ← buat tabel dulu sebelum window dibuat

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
