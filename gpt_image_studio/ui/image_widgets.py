import os
import shutil
import subprocess

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QCursor, QDragEnterEvent, QDropEvent, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from ..i18n import I18N
from ..image_utils import crop_square


class ImageChip(QFrame):
    remove_requested = pyqtSignal(str)

    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.path = path
        self.setFixedSize(54, 54)
        self.setStyleSheet("QFrame{background:transparent;border:none;}")

        self.thumb = QLabel(self)
        self.thumb.setObjectName("chip-thumb")
        self.thumb.setGeometry(0, 0, 54, 54)
        self.thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap(path)
        if not pix.isNull():
            self.thumb.setPixmap(crop_square(pix, 54))

        x_btn = QPushButton("×", self)
        x_btn.setGeometry(37, 0, 17, 17)
        x_btn.setStyleSheet("""
            QPushButton{background:#cc3333;border:none;border-radius:8px;
                color:#fff;font-size:11px;font-weight:bold;padding:0;}
            QPushButton:hover{background:#ff4444;}
        """)
        x_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        x_btn.clicked.connect(lambda: self.remove_requested.emit(self.path))
        x_btn.raise_()


# ─────────────────────── 拖拽上传区 ───────────────────────
class DropZone(QWidget):
    images_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.image_paths: list[str] = []
        self.setAcceptDrops(True)
        self.setFixedHeight(70)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # 空状态提示
        self._hint = QLabel(self._tr("drop_hint"))
        self._hint.setObjectName("drop-hint")
        self._hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._hint.mousePressEvent = lambda e: self._pick()
        outer.addWidget(self._hint)

        # 有图状态
        self._chip_row = QWidget()
        self._chip_row.setObjectName("drop-chip-row")
        cr = QHBoxLayout(self._chip_row)
        cr.setContentsMargins(10, 6, 10, 6); cr.setSpacing(8)
        self._chips = QHBoxLayout(); self._chips.setSpacing(8)
        cr.addLayout(self._chips)
        cr.addStretch()
        self.add_btn = QPushButton(self._tr("add_image"))
        self.add_btn.setObjectName("card-action-btn")
        self.add_btn.setFixedHeight(30)
        self.add_btn.clicked.connect(self._pick); cr.addWidget(self.add_btn)
        self._chip_row.setVisible(False)
        outer.addWidget(self._chip_row)

    def _pick(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, self._tr("pick_ref"), "", "Images (*.png *.jpg *.jpeg *.webp *.gif)"
        )
        if paths: self._add(paths)

    def _add(self, paths):
        for p in paths:
            if p not in self.image_paths: self.image_paths.append(p)
        self._rebuild()
        self.images_changed.emit(self.image_paths)

    def _remove(self, path):
        if path in self.image_paths: self.image_paths.remove(path)
        self._rebuild()
        self.images_changed.emit(self.image_paths)

    def _rebuild(self):
        while self._chips.count():
            item = self._chips.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        if self.image_paths:
            for p in self.image_paths:
                chip = ImageChip(p)
                chip.remove_requested.connect(self._remove)
                self._chips.addWidget(chip)
            self._hint.setVisible(False); self._chip_row.setVisible(True)
        else:
            self._hint.setVisible(True); self._chip_row.setVisible(False)

    def apply_theme(self):
        self._hint.style().unpolish(self._hint); self._hint.style().polish(self._hint)
        self._chip_row.style().unpolish(self._chip_row); self._chip_row.style().polish(self._chip_row)

    def _set_drag_highlight(self, on: bool):
        self._hint.setProperty("dragging", on)
        self._chip_row.setProperty("dragging", on)
        self.apply_theme()

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction(); self._set_drag_highlight(True)

    def dragLeaveEvent(self, e): self._set_drag_highlight(False)

    def dropEvent(self, e: QDropEvent):
        self._set_drag_highlight(False)
        paths = [
            url.toLocalFile() for url in e.mimeData().urls()
            if url.toLocalFile().lower().endswith((".png",".jpg",".jpeg",".webp",".gif"))
        ]
        if paths: self._add(paths)


# ─────────────────────── 图片结果卡片 ───────────────────────
class ImageCard(QFrame):
    preview_requested = pyqtSignal(int)
    edit_requested    = pyqtSignal(str)   # 传图片路径，触发"编辑此图"

    def __init__(self, path: str, index: int, parent=None):
        super().__init__(parent)
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.path = path; self.index = index
        self._orig_pix: QPixmap | None = None
        self.setObjectName("img-card"); self.setFixedSize(210, 258)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        v = QVBoxLayout(self); v.setContentsMargins(4,4,4,6); v.setSpacing(4)

        # 缩略图区
        self.thumb = QLabel()
        self.thumb.setObjectName("image-thumb")
        self.thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb.setFixedSize(202, 196)
        v.addWidget(self.thumb)

        # 操作按钮行
        br = QHBoxLayout(); br.setContentsMargins(0,0,0,0); br.setSpacing(4)
        for icon, tip, slot in [(self._tr("view"), self._tr("preview"), self._preview),
                                  (self._tr("edit"), self._tr("edit_this"), self._edit),
                                  (self._tr("save"), self._tr("save"), self._save),
                                  (self._tr("open"), self._tr("folder_tip"), self._reveal)]:
            b = QPushButton(icon); b.setObjectName("card-action-btn"); b.setToolTip(tip); b.setFixedSize(44,24)
            b.clicked.connect(slot); br.addWidget(b)
        br.addStretch()

        # 红底预览勾选框（放在按钮行右侧）
        self._red_chk = QPushButton(self._tr("red"))
        self._red_chk.setObjectName("red-bg-btn")
        self._red_chk.setCheckable(True)
        self._red_chk.setFixedSize(40, 24)
        self._red_chk.setToolTip(self._tr("red_tip"))
        self._red_chk.toggled.connect(self._on_red_toggled)
        br.addWidget(self._red_chk)
        v.addLayout(br)

        pix = QPixmap(path)
        if not pix.isNull():
            self._orig_pix = pix
        self._render_thumb(False)

    def _render_thumb(self, red: bool):
        if self._orig_pix is None or self._orig_pix.isNull():
            return
        scaled = self._orig_pix.scaled(
            QSize(202, 196),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        if red:
            composite = QPixmap(scaled.size())
            composite.fill(QColor("#cc2222"))
            p = QPainter(composite); p.drawPixmap(0, 0, scaled); p.end()
            self.thumb.setPixmap(composite)
            self.thumb.setProperty("red", True)
        else:
            self.thumb.setPixmap(scaled)
            self.thumb.setProperty("red", False)
        self.thumb.style().unpolish(self.thumb); self.thumb.style().polish(self.thumb)

    def _on_red_toggled(self, checked: bool):
        self._render_thumb(checked)

    # set_red_bg остаётся для обратной совместимости (рефреш не нужен)
    def set_red_bg(self, enabled: bool):
        pass   # 红底现在由每张卡片自己管理，全局接口保留为空

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton: self._preview()

    def _preview(self): self.preview_requested.emit(self.index)

    def _edit(self):
        self.edit_requested.emit(self.path)

    def _save(self):
        dest, _ = QFileDialog.getSaveFileName(
            self, self._tr("save"), os.path.basename(self.path),
            "PNG (*.png);;WebP (*.webp);;JPEG (*.jpg);;All Files (*)"
        )
        if dest:
            shutil.copy2(self.path, dest)

    def _reveal(self):
        subprocess.Popen(["explorer", "/select,", os.path.normpath(self.path)])


# ─────────────────────── 对话轮次气泡 ───────────────────────
class TurnWidget(QFrame):
    """展示一次生成请求：prompt + 结果图片"""
    preview_requested = pyqtSignal(list, int)  # all_paths, clicked_index
    edit_requested    = pyqtSignal(str)         # image_path → 填入编辑区

    def __init__(self, turn: dict, all_image_paths: list[str], base_index: int, parent=None):
        super().__init__(parent)
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.setObjectName("turn-frame")
        v = QVBoxLayout(self); v.setContentsMargins(12, 10, 12, 10); v.setSpacing(8)

        # prompt 行
        ph = QHBoxLayout(); ph.setSpacing(8)
        icon = QLabel("IMG"); icon.setFixedWidth(30)
        icon.setStyleSheet("color:#a78bfa;font-size:10px;font-weight:800;")
        ph.addWidget(icon)
        pl = QLabel(turn.get("prompt",""))
        pl.setObjectName("turn-prompt"); pl.setWordWrap(True)
        ph.addWidget(pl, 1)
        ts = turn.get("timestamp","")[:16].replace("T"," ")
        bg_tag = f"  bg={turn.get('background','')}" if turn.get("background") and turn.get("background") != "auto" else ""
        meta = QLabel(f"{turn.get('model','')}  {turn.get('size','')}{bg_tag}  {ts}")
        meta.setObjectName("turn-meta"); meta.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        ph.addWidget(meta)
        v.addLayout(ph)

        # 图片行
        images = turn.get("images", [])
        if images:
            img_row = QHBoxLayout(); img_row.setSpacing(8); img_row.setContentsMargins(28,0,0,0)
            for i, p in enumerate(images):
                if not os.path.exists(p): continue
                card = ImageCard(p, base_index + i, self)
                card.preview_requested.connect(
                    lambda idx, ap=all_image_paths: self.preview_requested.emit(ap, idx)
                )
                card.edit_requested.connect(self.edit_requested)
                img_row.addWidget(card)
            img_row.addStretch()
            v.addLayout(img_row)

