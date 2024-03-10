import sys
from PyQt5.QtWidgets import QApplication
from .views import Window
try:
    import pyi_splash
except ImportError:
    pass


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    try:
        pyi_splash.close()
    except:
        pass
    sys.exit(app.exec_())