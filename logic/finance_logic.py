"""
finance_logic.py — Layer logika bisnis
Hanya berisi kalkulasi, validasi, dan format.
Tidak ada SQL atau kode UI di sini.
"""

KATEGORI_PEMASUKAN   = ["Gaji", "Freelance", "Investasi", "Hadiah", "Lainnya"]
KATEGORI_PENGELUARAN = ["Makan & Minum", "Transportasi", "Belanja",
                        "Tagihan", "Hiburan", "Kesehatan", "Lainnya"]


def validasi(tanggal, tipe, kategori, jumlah):
    """Return (True, '') jika valid, atau (False, pesan_error)."""
    if not tanggal:
        return False, "Tanggal wajib diisi."
    if tipe not in ["Pemasukan", "Pengeluaran"]:
        return False, "Tipe tidak valid."
    if kategori not in KATEGORI_PEMASUKAN + KATEGORI_PENGELUARAN:
        return False, "Kategori tidak valid."
    if jumlah <= 0:
        return False, "Jumlah harus lebih dari 0."
    return True, ""


def hitung_ringkasan(rows):
    """Hitung total masuk, keluar, dan saldo. Return dict."""
    masuk  = sum(r["jumlah"] for r in rows if r["tipe"] == "Pemasukan")
    keluar = sum(r["jumlah"] for r in rows if r["tipe"] == "Pengeluaran")
    return {"masuk": masuk, "keluar": keluar, "saldo": masuk - keluar}


def format_rupiah(jumlah):
    """Format angka ke string Rupiah. Contoh: Rp 1.500.000"""
    prefix = "-" if jumlah < 0 else ""
    return f"{prefix}Rp {abs(jumlah):,.0f}".replace(",", ".")
