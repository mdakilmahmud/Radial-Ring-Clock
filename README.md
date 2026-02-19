# Radial-Ring-Clock
A smooth 60 FPS radial ring clock with real-time seconds and minutes rendered directly as a Windows live wallpaper.

The outer ring displays seconds.
The inner ring displays minutes.
The center displays the current hour.

The glowing effect occurs only when numbers pass inside the fixed viewport box at 3 o’clock.

This clock runs in real time using system time with microsecond precision.

---

## Features

- Real-time second and minute rotation
- Smooth 60 FPS animation
- Glow effect only inside viewport
- Transparent, click-through wallpaper layer
- Auto-sync with system time
- Scales automatically to screen resolution

---

## Requirements

- Windows OS
- Python 3.9+
- PyQt5
- pywin32

---

## Installation

1. Clone the repository:

   git clone https://github.com/YOUR_USERNAME/Radial-Ring-Clock.git

2. Enter the project folder:

   cd Radial-Ring-Clock

3. Install dependencies:

   pip install -r requirements.txt

---

## How to Run

Option 1 (Recommended):

Double-click:
start_clock.bat

Option 2 (Manual):

python Clock.py

---

## How It Works

The application attaches itself to the Windows WorkerW layer using win32 API.

This makes it behave like a live wallpaper.

The box at 3 o’clock is a fixed viewport.
The rings rotate behind it.
Numbers glow only when inside the viewport.

---

## Troubleshooting

### 1. ImportError: DLL load failed (PyQt5)

Run:

pip uninstall PyQt5
pip install PyQt5==5.15.9

Then try again.

---

### 2. pywin32 errors

Run:

pip install pywin32
python -m pywin32_postinstall install

Restart your PC.

---

### 3. Clock does not appear

- Make sure you are on Windows.
- Make sure no antivirus blocks Python.
- Try running as Administrator.

---

### 4. Wallpaper disappears after refresh

Restart the clock using start_clock.bat.

---

## Notes

This project is Windows-specific.
It uses Windows shell manipulation to attach to the wallpaper layer.

It will NOT work on:
- macOS
- Linux

---

## License

MIT License
