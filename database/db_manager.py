"""
db_manager.py — Layer database
Hanya berisi koneksi dan operasi SQLite.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "finance.db")
DB_PATH = os.path.abspath(DB_PATH)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal  TEXT NOT NULL,
                tipe     TEXT NOT NULL,
                kategori TEXT NOT NULL,
                jumlah   REAL NOT NULL,
                catatan  TEXT DEFAULT ''
            )
        """)
        conn.commit()
    finally:
        conn.close()


def tambah(tanggal, tipe, kategori, jumlah, catatan=""):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO transaksi (tanggal, tipe, kategori, jumlah, catatan) VALUES (?,?,?,?,?)",
            (tanggal, tipe, kategori, jumlah, catatan)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def ambil_semua():
    conn = get_conn()
    try:
        return conn.execute(
            "SELECT * FROM transaksi ORDER BY tanggal DESC, id DESC"
        ).fetchall()
    finally:
        conn.close()


def ambil_by_id(id_):                          # ← BARU: untuk isi form edit
    conn = get_conn()
    try:
        return conn.execute(
            "SELECT * FROM transaksi WHERE id=?", (id_,)
        ).fetchone()
    finally:
        conn.close()


def update(id_, tanggal, tipe, kategori, jumlah, catatan=""):   # ← BARU
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE transaksi SET tanggal=?, tipe=?, kategori=?, jumlah=?, catatan=? WHERE id=?",
            (tanggal, tipe, kategori, jumlah, catatan, id_)
        )
        conn.commit()
    finally:
        conn.close()


def hapus(id_):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM transaksi WHERE id=?", (id_,))
        conn.commit()
    finally:
        conn.close()
