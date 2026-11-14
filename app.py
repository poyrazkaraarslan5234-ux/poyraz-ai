# pip install PySide6 psutil
import sys, os, time, socket, platform, collections
import psutil
from PySide6.QtCore import Qt, QTimer, QProcess, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPlainTextEdit, QLineEdit)

CYAN, BG = "#aacfd1", "#05080d"

class Graph(QWidget):
    def __init__(self, title, n=60):
        super().__init__()
        self.title = title
        self.data = collections.deque([0] * n, maxlen=n)
        self.setMinimumHeight(120)

    def push(self, v):
        self.data.append(v)
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        p.setPen(QPen(QColor(CYAN), 1))
        p.drawRect(0, 0, w - 1, h - 1)
        p.setFont(QFont("Consolas", 9))
        p.drawText(8, 16, f"{self.title}  {self.data[-1]:.0f}%")
        p.setPen(QPen(QColor(CYAN), 2))
        step = w / (len(self.data) - 1)
        pts = [QPointF(i * step, h - 4 - (v / 100) * (h - 28))
               for i, v in enumerate(self.data)]
        for a, b in zip(pts, pts[1:]):
            p.drawLine(a, b)

class Terminal(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.out = QPlainTextEdit(readOnly=True)
        self.inp = QLineEdit()
        self.inp.setPlaceholderText("komut yaz, Enter'a bas")
        lay.addWidget(self.out)
        lay.addWidget(self.inp)
        self.proc = QProcess(self)
        self.proc.setProcessChannelMode(QProcess.MergedChannels)
        self.proc.readyRead.connect(self.read)
        self.proc.start("cmd.exe" if os.name == "nt" else "/bin/bash")
        self.inp.returnPressed.connect(self.send)

    def read(self):
        self.out.appendPlainText(bytes(self.proc.readAll()).decode(errors="ignore").rstrip())

    def send(self):
        self.proc.write((self.inp.text() + "\n").encode())
        self.inp.clear()

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDEX-PY")
        self.setStyleSheet(f"""
            QWidget {{ background:{BG}; color:{CYAN}; font-family:Consolas,monospace; }}
            QPlainTextEdit, QLineEdit {{ border:1px solid {CYAN}; padding:4px; }}
        """)
        root = QHBoxLayout(self)

        left = QVBoxLayout()
        self.cpu, self.ram = Graph("CPU"), Graph("RAM")
        left.addWidget(self.cpu); left.addWidget(self.ram); left.addStretch()

        right = QVBoxLayout()
        self.clock = QLabel(); self.clock.setFont(QFont("Consolas", 28))
        self.info = QLabel(); self.info.setAlignment(Qt.AlignTop)
        right.addWidget(self.clock); right.addWidget(self.info); right.addStretch()

        root.addLayout(left, 2)
        root.addWidget(Terminal(), 5)
        root.addLayout(right, 2)

        t = QTimer(self); t.timeout.connect(self.tick); t.start(1000)
        self.tick()

    def tick(self):
        self.cpu.push(psutil.cpu_percent())
        self.ram.push(psutil.virtual_memory().percent)
        self.clock.setText(time.strftime("%H:%M:%S"))
        net = psutil.net_io_counters()
        self.info.setText(
            f"HOST : {socket.gethostname()}\n"
            f"OS   : {platform.system()} {platform.release()}\n"
            f"UP   : {int(time.time() - psutil.boot_time()) // 3600} saat\n"
            f"SENT : {net.bytes_sent // 1048576} MB\n"
            f"RECV : {net.bytes_recv // 1048576} MB")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F11:
            self.showNormal() if self.isFullScreen() else self.showFullScreen()
        elif e.key() == Qt.Key_Escape:
            self.close()
