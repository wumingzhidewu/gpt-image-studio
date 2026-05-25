from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


def crop_square(pix: QPixmap, size: int) -> QPixmap:
    scaled = pix.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )
    x = (scaled.width()  - size) // 2
    y = (scaled.height() - size) // 2
    return scaled.copy(x, y, size, size)
