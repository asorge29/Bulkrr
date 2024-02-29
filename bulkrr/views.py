from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtGui
from .ui.window import Ui_Window
from pathlib import Path
from collections import deque

FILTERS = ";;".join(
    (
        "All Files (*)",
        "PNG Files (*.png)",
        "JPG Files (*.jpg)",
        "JPEG Files (*.jpeg)",
        "GIF Files (*.gif)",
        "BMP Files (*.bmp)",
        "TIFF Files (*.tiff)",
        "Text Files (*.txt)",
        "PDF Files (*.pdf)",
        "Python Files (*.py)",
        "MP3 Files (*.mp3)",
        "MP4 Files (*.mp4)",
        "AVI Files (*.avi)",
    )
)

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self._files = deque()
        self._filesCount = len(self._files)
        self._setupUI()
        self._connectSignalsSlots()
        self.setWindowIcon(QtGui.QIcon("Bulkrr_logo.jpeg"))

    def _setupUI(self):
        self.setupUi(self)
    
    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)

    def loadFiles(self):
        self.dstFileList.clear()
        if self.dirEdit.text():
            initDir = self.dirEdit.text()
        else:
            initDir = str(Path.home())
        files, filter = QFileDialog.getOpenFileNames(
            self, "Choose Files to Rename", initDir, filter=FILTERS
        )
        if len(files) > 0:
            fileExtension = filter[filter.index("*") : -1]
            self.extensionLabel.setText(fileExtension)
            srcDirName = str(Path(files[0]).parent)
            self.dirEdit.setText(srcDirName)
            for file in files:
                self._files.append(Path(file))
                self.srcFileList.addItem(file)
            self._filesCount = len(self._files)