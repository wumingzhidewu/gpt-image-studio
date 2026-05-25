import os
import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QPixmap, QShortcut
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)

from ..i18n import I18N


class PreviewDialog(QDialog):
    def __init__(self, paths: list, index: int = 0, parent=None):
        super().__init__(parent)
        self.paths = paths
        self.index = index
        self.zoom  = 1.0
        self._orig_pix = None
        self._drag_pos = None
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.theme = getattr(parent, "theme", "dark")

        self.setWindowTitle(self._tr("preview_title"))
        self.setModal(True)
        self.resize(1000, 800)
        self.setMinimumSize(600, 500)
        self._apply_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── 顶部工具栏 ──
        bar = QWidget(); bar.setObjectName("preview-toolbar"); bar.setFixedHeight(44)
        br = QHBoxLayout(bar); br.setContentsMargins(12, 0, 12, 0); br.setSpacing(8)

        self.counter = QLabel()
        self.counter.setObjectName("preview-counter")
        br.addWidget(self.counter)
        br.addStretch()

        def tbtn(text, slot, w=32):
            b = QPushButton(text); b.setObjectName("preview-btn"); b.setFixedSize(w, 28)
            b.clicked.connect(slot); br.addWidget(b)
        tbtn("−", self._zoom_out)
        self.zoom_label = QPushButton("100%"); self.zoom_label.setObjectName("preview-btn"); self.zoom_label.setFixedSize(48, 28)
        self.zoom_label.clicked.connect(self._zoom_fit)
        br.addWidget(self.zoom_label)
        tbtn("+", self._zoom_in)
        br.addSpacing(6)

        save_btn = QPushButton(self._tr("save")); save_btn.setObjectName("preview-btn"); save_btn.setFixedHeight(28)
        save_btn.clicked.connect(self._save); br.addWidget(save_btn)

        close_btn = QPushButton("✕"); close_btn.setObjectName("preview-close-btn"); close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.reject); br.addWidget(close_btn)
        layout.addWidget(bar)

        # ── 图片显示区：用 QScrollArea 包 QLabel ──
        self.scroll = QScrollArea()
        self.scroll.setObjectName("preview-canvas")
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setStyleSheet("background:transparent;")
        self.scroll.setWidget(self.img_label)
        layout.addWidget(self.scroll, 1)

        # ── 底部导航 ──
        nav = QWidget(); nav.setObjectName("preview-nav"); nav.setFixedHeight(50)
        nr = QHBoxLayout(nav); nr.setContentsMargins(20, 0, 20, 0); nr.setSpacing(12)
        nr.addStretch()
        for txt, slot in [(self._tr("prev"), self._prev), (self._tr("next"), self._next)]:
            b = QPushButton(txt); b.setObjectName("preview-btn"); b.setFixedHeight(32)
            b.clicked.connect(slot); nr.addWidget(b)
        nr.addStretch()
        layout.addWidget(nav)

        # 快捷键
        for key, fn in [("Left", self._prev), ("Right", self._next),
                        ("Escape", self.reject), ("=", self._zoom_in),
                        ("-", self._zoom_out), ("F", self._zoom_fit)]:
            QShortcut(QKeySequence(key), self).activated.connect(fn)

        # 滚轮缩放 —— 在 scroll area 上安装事件过滤
        self.scroll.viewport().installEventFilter(self)
        self._load_current()

    def _apply_theme(self):
        dark = self.theme != "light"
        bg = "#0a0a0a" if dark else "#f6f8fb"
        bar_bg = "#111111" if dark else "#ffffff"
        border = "#1e1e1e" if dark else "#dbe2ea"
        btn_bg = "#1e1e1e" if dark else "#f8fafc"
        btn_hover = "#2a2a2a" if dark else "#eef2ff"
        text = "#aaaaaa" if dark else "#334155"
        text_hover = "#ffffff" if dark else "#111827"
        disabled = "#333333" if dark else "#cbd5e1"
        self.setStyleSheet(f"""
            QDialog{{background:{bg};}}
            #preview-toolbar{{background:{bar_bg};border-bottom:1px solid {border};}}
            #preview-nav{{background:{bar_bg};border-top:1px solid {border};}}
            #preview-counter{{color:{text};font-size:12px;}}
            #preview-btn{{background:{btn_bg};border:1px solid {border};
                border-radius:8px;color:{text};font-size:12px;padding:0 12px;}}
            #preview-btn:hover{{background:{btn_hover};color:{text_hover};}}
            #preview-btn:disabled{{color:{disabled};}}
            #preview-close-btn{{background:transparent;border:none;color:{disabled};font-size:14px;}}
            #preview-close-btn:hover{{color:#ef4444;}}
            #preview-canvas{{background:#0a0a0a;border:none;}}
        """)

    def eventFilter(self, obj, event):
        if obj is self.scroll.viewport() and event.type() == event.Type.Wheel:
            delta = event.angleDelta().y()
            if delta > 0:
                self._zoom_in()
            else:
                self._zoom_out()
            return True
        return super().eventFilter(obj, event)

    def _load_current(self):
        self._orig_pix = QPixmap(self.paths[self.index])
        self._zoom_fit()   # 默认适配窗口大小
        self.counter.setText(
            f"{self.index+1} / {len(self.paths)}  —  "
            f"{os.path.basename(self.paths[self.index])}"
        )

    def _render(self):
        if not self._orig_pix or self._orig_pix.isNull():
            self.img_label.setText(self._tr("load_failed")); return
        w = int(self._orig_pix.width()  * self.zoom)
        h = int(self._orig_pix.height() * self.zoom)
        scaled = self._orig_pix.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.img_label.setPixmap(scaled)
        self.img_label.resize(scaled.width(), scaled.height())
        pct = int(self.zoom * 100)
        self.zoom_label.setText(f"{pct}%")

    def _zoom_fit(self):
        """缩放到刚好能完整显示整张图"""
        if not self._orig_pix or self._orig_pix.isNull(): return
        vw = self.scroll.viewport().width()  - 8
        vh = self.scroll.viewport().height() - 8
        iw = self._orig_pix.width()
        ih = self._orig_pix.height()
        if iw == 0 or ih == 0: return
        self.zoom = min(vw / iw, vh / ih, 1.0)   # 不超过原始 100%
        self._render()

    def _zoom_in(self):
        self.zoom = min(self.zoom * 1.2, 8.0); self._render()

    def _zoom_out(self):
        self.zoom = max(self.zoom / 1.2, 0.05); self._render()

    def _prev(self):
        if self.index > 0:
            self.index -= 1; self._load_current()

    def _next(self):
        if self.index < len(self.paths) - 1:
            self.index += 1; self._load_current()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        # 如果当前是 fit 模式，随窗口大小自动重新适配
        if self._orig_pix and not self._orig_pix.isNull():
            self._zoom_fit()

    def _save(self):
        src = self.paths[self.index]
        dest, _ = QFileDialog.getSaveFileName(
            self, self._tr("save"), os.path.basename(src),
            "PNG (*.png);;WebP (*.webp);;JPEG (*.jpg);;All Files (*)"
        )
        if dest:
            shutil.copy2(src, dest)

