import sys

from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import QApplication

from .paths import LOGO_PATH, ensure_app_dirs
from .ui.main_window import MainWindow


# ─────────────────────── 入口 ───────────────────────
def main():
    ensure_app_dirs()
    app = QApplication(sys.argv)
    app.setApplicationName("GPT-Image Studio")
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))
    app.setStyle("Fusion")

    pal = QPalette()
    for role, color in [
        (QPalette.ColorRole.Window,          "#0d0d0d"),
        (QPalette.ColorRole.WindowText,      "#e8e8e8"),
        (QPalette.ColorRole.Base,            "#161616"),
        (QPalette.ColorRole.AlternateBase,   "#121212"),
        (QPalette.ColorRole.ToolTipBase,     "#161616"),
        (QPalette.ColorRole.ToolTipText,     "#dddddd"),
        (QPalette.ColorRole.Text,            "#e8e8e8"),
        (QPalette.ColorRole.Button,          "#1e1e1e"),
        (QPalette.ColorRole.ButtonText,      "#c8c8c8"),
        (QPalette.ColorRole.BrightText,      "#ff4040"),
        (QPalette.ColorRole.Link,            "#7b2ff7"),
        (QPalette.ColorRole.Highlight,       "#5a1eb4"),
        (QPalette.ColorRole.HighlightedText, "#ffffff"),
    ]:
        pal.setColor(role, QColor(color))
    app.setPalette(pal)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())
