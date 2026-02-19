import sys
import math
import datetime
import win32gui
import win32con
import win32api
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QTimer

class RadialClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radial Ring Clock Wallpaper")
        
        # Set window as a transparent, click-through background layer
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground) 
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Timer for 60 frames per second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)
        
        self.init_wallpaper_layer()

    def init_wallpaper_layer(self):
        hwnd = int(self.winId())
        progman = win32gui.FindWindow("Progman", None)
        win32gui.SendMessageTimeout(progman, 0x052C, 0, 0, win32con.SMTO_NORMAL, 1000)

        def enum_handler(h, hwnds):
            hwnds.append(h)
        hwnds = []
        win32gui.EnumWindows(enum_handler, hwnds)
        
        workerw = None
        for h in hwnds:
            if win32gui.FindWindowEx(h, 0, "SHELLDLL_DefView", None):
                workerw = win32gui.FindWindowEx(0, h, "WorkerW", None)
                break
        
        if workerw:
            win32gui.SetParent(hwnd, workerw)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(0, 0, 0, 0)) # Clean transparent background

        cx, cy = self.width() // 2, self.height() // 2
        min_dim = min(self.width(), self.height())
        R_SEC = int(min_dim * 0.416)
        R_MIN = int(min_dim * 0.305)

        # --- PRECISE TIME SYNC ---
        now = datetime.datetime.now()
        
        # Convert precise time to rotation (6 degrees per unit)
        sec_val = now.second + (now.microsecond / 1000000.0)
        min_val = now.minute + (sec_val / 60.0)
        hour_val = now.hour

        # The rotation is based on the value itself
        sec_rot = sec_val * 6
        min_rot = min_val * 6

        self.draw_ring(p, cx, cy, R_SEC, sec_rot)
        self.draw_ring(p, cx, cy, R_MIN, min_rot, dim=True)
        self.draw_box(p, cx, cy, R_SEC)

        # Center Hour
        p.setPen(QColor(255, 255, 255))
        p.setFont(QFont("Arial", int(min_dim * 0.105), QFont.Bold))
        p.drawText(self.rect(), Qt.AlignCenter, f"{hour_val:02d}")

    def draw_ring(self, p, cx, cy, radius, rotation, dim=False):
        BOX_WIDTH = 12
        for i in range(60):
            base_angle = i * 6
            
            # 1. VISUAL POSITION: 
            # We subtract rotation to move the numbers backward as time moves forward.
            # We subtract 90 to put the current value at the 3 o'clock position box.
            angle_deg = base_angle - rotation
            angle = math.radians(angle_deg)
            
            # 2. GLOW SENSOR:
            # We want to know if 'base_angle' matches the 'rotation' exactly.
            # The modulo 360 handles the wrap-around.
            rel = (base_angle - rotation) % 360
            if rel > 180: rel = 360 - rel

            inside_box = rel < (BOX_WIDTH / 2)
            glow = 255 if inside_box else (60 if dim else 110)
            scale = 1.3 if inside_box else 1.0

            color = QColor(glow, glow, glow)
            major = (i % 5 == 0)
            tick_len = radius * 0.07 if major else radius * 0.035
            
            x1 = cx + (radius - tick_len) * math.cos(angle)
            y1 = cy + (radius - tick_len) * math.sin(angle)
            x2 = cx + radius * math.cos(angle)
            y2 = cy + radius * math.sin(angle)

            p.setPen(QPen(color, max(1, int(radius * 0.01)) * (3 if major else 1)))
            p.drawLine(int(x1), int(y1), int(x2), int(y2))

            if major:
                tx = cx + (radius - radius * 0.154) * math.cos(angle)
                ty = cy + (radius - radius * 0.154) * math.sin(angle)
                f_size = int(radius * 0.060 * scale)
                p.setFont(QFont("Arial", f_size, QFont.Bold))
                p.setPen(color)
                p.drawText(int(tx - f_size * 0.7), int(ty + f_size * 0.6), f"{i:02d}")

    def draw_box(self, p, cx, cy, radius):
        w, h = int(radius * 0.567), int(radius * 0.160)
        # Shift ensures the box is centered on the 3 o'clock line
        shift = int(radius * 0.23)
        path = QPainterPath()
        # The box is physically placed at 0 degrees (3 o'clock)
        path.addRoundedRect(cx + radius - w // 2 - shift, cy - h // 2, w, h, h // 2, h // 2)
        p.setPen(QPen(QColor(120, 255, 0), max(2, int(radius * 0.013))))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = RadialClock()
    w.show()
    sys.exit(app.exec_())