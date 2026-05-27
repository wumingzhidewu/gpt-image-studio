from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class TemplateCard(QFrame):
    selected = pyqtSignal(str)
    activated = pyqtSignal(str)

    def __init__(self, template: dict, parent=None):
        super().__init__(parent)
        self.template = template
        self.setObjectName("template-card")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(158)

        v = QVBoxLayout(self); v.setContentsMargins(8,8,8,8); v.setSpacing(7)
        img = QLabel(); img.setObjectName("template-image"); img.setFixedHeight(108)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p = template.get("image")
        if p and Path(p).exists():
            pix = QPixmap(str(p)).scaled(
                240, 108,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            img.setPixmap(pix)
        v.addWidget(img)
        title = QLabel(template.get("title", "模板"))
        title.setObjectName("template-title")
        v.addWidget(title)
        prompt = QLabel(template.get("prompt", ""))
        prompt.setObjectName("template-prompt")
        prompt.setWordWrap(True)
        prompt.setMaximumHeight(34)
        v.addWidget(prompt)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.selected.emit(self.template.get("prompt", ""))

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.activated.emit(self.template.get("prompt", ""))
