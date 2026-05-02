"""
transaksi_dialog.py — Dialog untuk tambah DAN edit transaksi
data=None  → mode Tambah
data=dict  → mode Edit (form diisi otomatis)
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox,
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import QDate, Qt

from logic.finance_logic import (
    KATEGORI_PEMASUKAN, KATEGORI_PENGELUARAN, validasi
)


class TransaksiDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data  = data          # None = tambah, dict = edit
        self.hasil = None

        judul = "✏️  Edit Transaksi" if data else "💸  Tambah Transaksi"
        self.setWindowTitle(judul)
        self.setFixedSize(380, 320)
        self.setWindowModality(Qt.ApplicationModal)
        self._build_ui()

        if data:
            self._isi_form(data)   # isi form jika mode edit

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.setContentsMargins(20, 20, 20, 20)

        # Judul dialog
        judul_txt = "✏️  Edit Transaksi" if self.data else "💸  Tambah Transaksi"
        lbl = QLabel(judul_txt)
        lbl.setObjectName("dialogTitle")
        lbl.setAlignment(Qt.AlignCenter)
        root.addWidget(lbl)

        # ── Form (QFormLayout) ────────────────────────────────────────────
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        self.inp_tanggal = QDateEdit(QDate.currentDate())
        self.inp_tanggal.setCalendarPopup(True)
        self.inp_tanggal.setDisplayFormat("dd/MM/yyyy")
        self.inp_tanggal.setMaximumDate(QDate.currentDate())

        self.inp_tipe = QComboBox()
        self.inp_tipe.addItems(["Pemasukan", "Pengeluaran"])
        self.inp_tipe.currentTextChanged.connect(self._update_kategori)

        self.inp_kategori = QComboBox()
        self._update_kategori()

        self.inp_jumlah = QDoubleSpinBox()
        self.inp_jumlah.setRange(1, 999_999_999)
        self.inp_jumlah.setDecimals(0)
        self.inp_jumlah.setSingleStep(10_000)
        self.inp_jumlah.setPrefix("Rp ")
        self.inp_jumlah.setValue(100_000)
        self.inp_jumlah.setGroupSeparatorShown(True)

        self.inp_catatan = QLineEdit()
        self.inp_catatan.setPlaceholderText("Opsional, maks 100 karakter")
        self.inp_catatan.setMaxLength(100)

        form.addRow("Tanggal :",  self.inp_tanggal)
        form.addRow("Tipe :",     self.inp_tipe)
        form.addRow("Kategori :", self.inp_kategori)
        form.addRow("Jumlah :",   self.inp_jumlah)
        form.addRow("Catatan :",  self.inp_catatan)
        root.addLayout(form)

        # ── Tombol ───────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_simpan = QPushButton("💾  Simpan")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.clicked.connect(self._on_simpan)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.clicked.connect(self.reject)

        btn_row.addWidget(self.btn_simpan)
        btn_row.addWidget(self.btn_batal)
        root.addLayout(btn_row)

    def _update_kategori(self):
        self.inp_kategori.clear()
        if self.inp_tipe.currentText() == "Pemasukan":
            self.inp_kategori.addItems(KATEGORI_PEMASUKAN)
        else:
            self.inp_kategori.addItems(KATEGORI_PENGELUARAN)

    def _isi_form(self, data):
        """Isi semua field dengan data yang dipilih (mode edit)."""
        # Tipe dulu sebelum kategori agar dropdown kategori benar
        idx_tipe = self.inp_tipe.findText(data["tipe"])
        if idx_tipe >= 0:
            self.inp_tipe.setCurrentIndex(idx_tipe)
        self._update_kategori()

        tanggal = QDate.fromString(data["tanggal"], "yyyy-MM-dd")
        self.inp_tanggal.setDate(tanggal)

        idx_kat = self.inp_kategori.findText(data["kategori"])
        if idx_kat >= 0:
            self.inp_kategori.setCurrentIndex(idx_kat)

        self.inp_jumlah.setValue(float(data["jumlah"]))
        self.inp_catatan.setText(data["catatan"] or "")

    def _on_simpan(self):
        tanggal  = self.inp_tanggal.date().toString("yyyy-MM-dd")
        tipe     = self.inp_tipe.currentText()
        kategori = self.inp_kategori.currentText()
        jumlah   = self.inp_jumlah.value()

        ok, pesan = validasi(tanggal, tipe, kategori, jumlah)
        if not ok:
            QMessageBox.warning(self, "⚠️  Validasi", pesan)
            return

        self.hasil = {
            "tanggal":  tanggal,
            "tipe":     tipe,
            "kategori": kategori,
            "jumlah":   jumlah,
            "catatan":  self.inp_catatan.text().strip()
        }
        self.accept()
