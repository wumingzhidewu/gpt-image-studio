import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from ..image_utils import crop_square
from ..paths import LOGO_PATH


class SessionItem(QFrame):
    clicked_signal = pyqtSignal(str)   # session id

    def __init__(self, session: dict, active: bool = False, parent=None):
        super().__init__(parent)
        self.sid = session["id"]
        self.setObjectName("session-item-active" if active else "session-item")
        self.setMinimumHeight(70)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        row = QHBoxLayout(self); row.setContentsMargins(10,8,10,8); row.setSpacing(10)

        thumb = QLabel(); thumb.setObjectName("session-thumb"); thumb.setFixedSize(52,52)
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        first_img = None
        for t in session.get("turns",[]):
            imgs = t.get("images",[])
            if imgs and os.path.exists(imgs[0]):
                first_img = imgs[0]; break
        if first_img:
            thumb.setPixmap(crop_square(QPixmap(first_img), 52))
        elif LOGO_PATH.exists():
            thumb.setPixmap(crop_square(QPixmap(str(LOGO_PATH)), 52))
        else:
            thumb.setText("IMG")
        row.addWidget(thumb)

        col = QVBoxLayout(); col.setSpacing(4); col.setContentsMargins(0,0,0,0)
        turns = session.get("turns",[])
        last_prompt = turns[-1].get("prompt","") if turns else ""
        title = session.get("title") or last_prompt or "新生成"
        tl = QLabel(title)
        tl.setObjectName("session-title")
        tl.setWordWrap(True)
        tl.setMaximumHeight(34)
        col.addWidget(tl)
        ts = session.get("updated","")[:16].replace("T"," ")
        ml = QLabel(f"{len(turns)} 张图 · {ts}")
        ml.setObjectName("session-meta")
        col.addWidget(ml)
        row.addLayout(col, 1)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked_signal.emit(self.sid)

