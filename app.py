# pip install PySide6 psutil
import sys, socket, hashlib, ipaddress, time
from concurrent.futures import ThreadPoolExecutor
import psutil
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton,
    QCheckBox, QPlainTextEdit, QFileDialog, QHeaderView)

CYAN, BG, WARN = "#aacfd1", "#05080d", "#ff9f43"

def log(widget, msg):
    widget.appendPlainText(f"[{time.strftime('%H:%M:%S')}] {msg}")

# ---------- Bağlantı izleyici ----------
class ConnTab(QWidget):
    def __init__(self, logbox):
        super().__init__()
        self.logbox = logbox
        lay = QVBoxLayout(self)
        self.summary = QLabel()
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Proto", "Yerel", "Uzak", "Durum", "PID", "Süreç"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.summary)
        lay.addWidget(self.table)
        t = QTimer(self); t.timeout.connect(self.refresh); t.start(2000)
        self.refresh()

    def refresh(self):
        try:
            conns = psutil.net_connections(kind="inet")
        except psutil.AccessDenied:
            self.summary.setText("Erişim reddedildi: yönetici/root olarak çalıştır.")
            return
        exposed = 0
        self.table.setRowCount(len(conns))
        for r, c in enumerate(conns):
            proto = "TCP" if c.type == socket.SOCK_STREAM else "UDP"
            local = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "-"
            remote = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "-"
            try:
                name = psutil.Process(c.pid).name() if c.pid else "-"
            except psutil.Error:
                name = "?"
            row = [proto, local, remote, c.status, str(c.pid or "-"), name]
            is_exposed = (c.status == "LISTEN" and c.laddr
                          and c.laddr.ip in ("0.0.0.0", "::"))
            exposed += bool(is_exposed)
            for col, val in enumerate(row):
                item = QTableWidgetItem(val)
                if is_exposed:
                    item.setForeground(QColor(WARN))
                self.table.setItem(r, col, item)
        self.summary.setText(
            f"Toplam bağlantı: {len(conns)}  |  Tüm arayüzlere açık dinleyen port: {exposed}")

# ---------- Port tarayıcı (sadece özel ağ / loopback) ----------
class Scanner(QThread):
    found = Signal(int, str)
    finished_scan = Signal(int)

    def __init__(self, host, ports):
        super().__init__()
        self.host, self.ports = host, ports
        self._stop = False

    def stop(self): self._stop = True

    def run(self):
        count = 0
        def probe(p):
            nonlocal count
            if self._stop: return
            with socket.socket() as s:
                s.settimeout(0.4)
                if s.connect_ex((self.host, p)) == 0:
                    try: name = socket.getservbyport(p)
                    except OSError: name = "bilinmiyor"
                    count += 1
                    self.found.emit(p, name)
        with ThreadPoolExecutor(100) as ex:
            list(ex.map(probe, self.ports))
        self.finished_scan.emit(count)

class ScanTab(QWidget):
    def __init__(self, logbox):
        super().__init__()
        self.logbox, self.worker = logbox, None
        lay = QVBoxLayout(self)
        row = QHBoxLayout()
        self.host = QLineEdit("127.0.0.1")
        self.start_p, self.end_p = QLineEdit("1"), QLineEdit("1024")
        row.addWidget(QLabel("Hedef:")); row.addWidget(self.host)
        row.addWidget(QLabel("Port:")); row.addWidget(self.start_p)
        row.addWidget(QLabel("-")); row.addWidget(self.end_p)
        self.auth = QCheckBox("Bu sistemi test etme yetkim var")
        self.btn = QPushButton("Taramayı Başlat")
        self.btn.clicked.connect(self.start)
        self.out = QPlainTextEdit(readOnly=True)
        lay.addLayout(row); lay.addWidget(self.auth)
        lay.addWidget(self.btn); lay.addWidget(self.out)

    def start(self):
        if not self.auth.isChecked():
            self.out.appendPlainText("Önce yetki onayını işaretle."); return
        try:
            ip = ipaddress.ip_address(socket.gethostbyname(self.host.text().strip()))
            a, b = int(self.start_p.text()), int(self.end_p.text())
            assert 1 <= a <= b <= 65535 and b - a <= 10000
        except Exception:
            self.out.appendPlainText("Geçersiz hedef veya port aralığı (en fazla 10000 port)."); return
        if not (ip.is_private or ip.is_loopback):
            self.out.appendPlainText("Bu araç sadece özel ağ/localhost adreslerini tarar."); return
        self.out.clear(); self.btn.setEnabled(False)
        log(self.logbox, f"Tarama: {ip} {a}-{b}")
        self.worker = Scanner(str(ip), range(a, b + 1))
        self.worker.found.connect(lambda p, n: self.out.appendPlainText(f"AÇIK  {p}/tcp  ({n})"))
        self.worker.finished_scan.connect(self.done)
        self.worker.start()

    def done(self, n):
        self.out.appendPlainText(f"\nTarama bitti. Açık port: {n}")
        log(self.logbox, f"Tarama bitti, açık port: {n}")
        self.btn.setEnabled(True)

# ---------- Dosya bütünlüğü ----------
class HashTab(QWidget):
    def __init__(self, logbox):
        super().__init__()
        self.logbox = logbox
        lay = QVBoxLayout(self)
        self.btn = QPushButton("Dosya Seç ve SHA-256 Hesapla")
        self.btn.clicked.connect(self.pick)
        self.expected = QLineEdit(); self.expected.setPlaceholderText("Beklenen hash (isteğe bağlı)")
        self.out = QPlainTextEdit(readOnly=True)
        lay.addWidget(self.btn); lay.addWidget(self.expected); lay.addWidget(self.out)

    def pick(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya seç")
        if not path: return
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        digest = h.hexdigest()
        exp = self.expected.text().strip().lower()
        verdict = ""
        if exp:
            verdict = "\nSONUÇ: EŞLEŞTİ ✔" if exp == digest else "\nSONUÇ: EŞLEŞMEDİ ✘ (dosya değişmiş olabilir)"
        self.out.setPlainText(f"{path}\nSHA-256: {digest}{verdict}")
        log(self.logbox, f"Hash hesaplandı: {path}")

# ---------- Ana pencere ----------
class Main(QWidget):
