from PyQt5.QtGui import QPalette, QBrush, QPixmap, QColor
from PyQt5.QtCore import Qt

class BackgroundCustomizer:
    def __init__(self, background_image_path=None, background_color=QColor(255, 255, 255)):
        self.background_image_path = background_image_path
        self.background_color = background_color

    def apply_background(self, widget):
        palette = widget.palette()
        if self.background_image_path:
            pixmap = QPixmap(self.background_image_path)
            palette.setBrush(widget.backgroundRole(), QBrush(pixmap))
        elif self.background_color:
            palette.setColor(widget.backgroundRole(), self.background_color)
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)