from PyQt5.QtWidgets import QWidget
from .ui.window import Ui_Window

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def _setupUI(self):
        self._setupUI(self)