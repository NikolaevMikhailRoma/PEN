from PyQt5 import QtGui, QtCore

class BackgroundCustomizer:
    def __init__(self, background_image_path=None, background_color=QtGui.QColor(255, 255, 255)):
        self.background_image_path = background_image_path
        self.background_color = background_color

    def apply_background(self, widget):
        palette = widget.palette()
        if self.background_image_path:
            pixmap = QtGui.QPixmap(self.background_image_path)
            palette.setBrush(widget.backgroundRole(), QtGui.QBrush(pixmap))
        elif self.background_color:
            palette.setColor(widget.backgroundRole(), self.background_color)
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)