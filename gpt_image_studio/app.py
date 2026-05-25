import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from .config import load_config
from .paths import LOGO_PATH, ensure_app_dirs
from .styles import apply_app_palette
from .ui.main_window import MainWindow


# ─────────────────────── 入口 ───────────────────────
def main():
    ensure_app_dirs()
    app = QApplication(sys.argv)
    app.setApplicationName("GPT-Image Studio")
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    app.setStyle("Fusion")

    cfg = load_config()
    apply_app_palette(app, cfg.get("theme", "dark"))

    win = MainWindow()
    win.show()
    sys.exit(app.exec())
