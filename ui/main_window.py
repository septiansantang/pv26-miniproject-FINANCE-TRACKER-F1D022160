"""
main_window.py — Layer UI jendela utama
Hanya menampilkan data. Form tambah/edit ada di TransaksiDialog.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor

from database.db_manager import init_db, tambah, ambil_semua, ambil_by_id, update, hapus
from logic.finance_logic import hitung_ringkasan, format_rupiah
from ui.transaksi_dialog import TransaksiDialog

NAMA = "SEPTIAN DWI SAPUTRA"
NIM  = "F1D022160"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.setWindowTitle("FinTrack Mini — Pengelola Keuangan")
        self.resize(820, 540)
        self._build_menubar()
        self._build_ui()
        self._load()

    # ── Menu Bar ──────────────────────────────────────────────────────────────
    def _build_menubar(self):
        mb = self.menuBar()

        m_file = mb.addMenu("&File")
        act_keluar = QAction("Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        m_file.addAction(act_keluar)

        m_bantuan = mb.addMenu("&Bantuan")
        act_tentang = QAction("Tentang Aplikasi", self)
        act_tentang.triggered.connect(self._tentang)
        m_bantuan.addAction(act_tentang)

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(10)
        root.setContentsMargins(14, 10, 14, 10)

        # Identitas
        lbl_id = QLabel(f"👤  {NAMA}   |   NIM: {NIM}")
        lbl_id.setObjectName("labelIdentitas")
        lbl_id.setAlignment(Qt.AlignCenter)
        lbl_id.setTextInteractionFlags(Qt.NoTextInteraction)
        root.addWidget(lbl_id)

        # Saldo
        self.lbl_saldo = QLabel("💰  Saldo: Rp 0")
        self.lbl_saldo.setObjectName("labelSaldo")
        self.lbl_saldo.setAlignment(Qt.AlignCenter)
        root.addWidget(self.lbl_saldo)

        # ── Tombol aksi ───────────────────────────────────────────────────
        aksi_row = QHBoxLayout()

        self.btn_tambah = QPushButton("➕  Tambah")
        self.btn_tambah.setObjectName("btnSimpan")
        self.btn_tambah.clicked.connect(self._on_tambah)       # signal→slot

        self.btn_edit = QPushButton("✏️  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setEnabled(False)
        self.btn_edit.clicked.connect(self._on_edit)           # signal→slot

        self.btn_hapus = QPushButton("🗑  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setEnabled(False)
        self.btn_hapus.clicked.connect(self._on_hapus)         # signal→slot

        self.lbl_total = QLabel("0 transaksi")
        self.lbl_total.setObjectName("labelCount")

        aksi_row.addWidget(self.btn_tambah)
        aksi_row.addWidget(self.btn_edit)
        aksi_row.addWidget(self.btn_hapus)
        aksi_row.addStretch()
        aksi_row.addWidget(self.lbl_total)
        root.addLayout(aksi_row)

        # ── Tabel ─────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setObjectName("dataTable")
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tanggal", "Tipe", "Kategori", "Jumlah", "Catatan"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self._on_pilih)  # signal→slot
        root.addWidget(self.table)

        self.statusBar().showMessage(f"  {NAMA}  |  NIM: {NIM}")

    # ── Slots ─────────────────────────────────────────────────────────────────
    def _on_pilih(self):
        dipilih = bool(self.table.selectedItems())
        self.btn_edit.setEnabled(dipilih)
        self.btn_hapus.setEnabled(dipilih)

    def _on_tambah(self):
        dialog = TransaksiDialog(self)
        if dialog.exec():
            tambah(**dialog.hasil)
            self._load()

    def _on_edit(self):
        row = self.table.currentRow()
        if row < 0:
            return
        id_  = int(self.table.item(row, 0).text())
        data = dict(ambil_by_id(id_))              # ambil data dari DB
        dialog = TransaksiDialog(self, data=data)  # buka dialog isi data lama
        if dialog.exec():
            update(id_, **dialog.hasil)            # simpan perubahan ke DB
            self._load()

    def _on_hapus(self):
        row = self.table.currentRow()
        if row < 0:
            return
        id_  = int(self.table.item(row, 0).text())
        kat  = self.table.item(row, 3).text()
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Yakin hapus transaksi «{kat}»?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            hapus(id_)
            self._load()

    def _load(self):
        rows = ambil_semua()

        self.table.setRowCount(0)
        for rd in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, key in enumerate(['id','tanggal','tipe','kategori','jumlah','catatan']):
                val  = rd[key]
                text = format_rupiah(val) if key == 'jumlah' else str(val or "")
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if key == 'tipe':
                    item.setForeground(
                        QColor("#1b5e20" if val == "Pemasukan" else "#b71c1c")
                    )
                self.table.setItem(r, c, item)

        self.lbl_total.setText(f"{self.table.rowCount()} transaksi")

        ring = hitung_ringkasan(rows)
        self.lbl_saldo.setText(
            f"💰 Saldo: {format_rupiah(ring['saldo'])}"
            f"   |   💚 Masuk: {format_rupiah(ring['masuk'])}"
            f"   |   ❤️ Keluar: {format_rupiah(ring['keluar'])}"
        )
        obj = "labelSaldoMinus" if ring["saldo"] < 0 else "labelSaldo"
        self.lbl_saldo.setObjectName(obj)
        self.lbl_saldo.style().unpolish(self.lbl_saldo)
        self.lbl_saldo.style().polish(self.lbl_saldo)

    def _tentang(self):
        QMessageBox.about(self, "Tentang Aplikasi",
            f"<h3>💰 FinTrack Mini</h3>"
            f"<p>Aplikasi pengelola keuangan pribadi sederhana.<br>"
            f"Dibuat dengan PySide6 dan SQLite.</p><hr>"
            f"<b>Nama:</b> {NAMA}<br><b>NIM :</b> {NIM}"
        )
