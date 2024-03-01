from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from .ui.window import Ui_Window
from .rename import Renamer
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
        self._updateStateWhenNoFiles()

    def _updateStateWhenNoFiles(self):
        self._filesCount = len(self._files)
        self.loadFilesButton.setEnabled(True)
        self.loadFilesButton.setFocus(True)
        self.renameFilesButton.setEnabled(False)
        self.prefixEdit.clear()
        self.prefixEdit.setEnabled(False)

    def _updateStateWhenFilesLoaded(self):
        self.prefixEdit.setEnabled(True)
        self.prefixEdit.setFocus(True)

    def _updateStateWhenReady(self):
        if self.prefixEdit.text():
            self.renameFilesButton.setEnabled(True)
        else:
            self.renameFilesButton.setEnabled(False)

    def _updateStateWhileRenaming(self):
        self.loadFilesButton.setEnabled(False)
        self.renameFilesButton.setEnabled(False)
    
    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
        self.renameFilesButton.clicked.connect(self.renameFiles)
        self.prefixEdit.textChanged.connect(self._updateStateWhenReady)

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
            self._updateStateWhenFilesLoaded()
            fileExtension = filter[filter.index("*") : -1]
            self.extensionLabel.setText(fileExtension)
            srcDirName = str(Path(files[0]).parent)
            self.dirEdit.setText(srcDirName)
            for file in files:
                self._files.append(Path(file))
                self.srcFileList.addItem(file)
            self._filesCount = len(self._files)
    
    def renameFiles(self):
        self._runRenamerThread()
        self._updateStateWhileRenaming()

    def _runRenamerThread(self):
        prefix = self.prefixEdit.text()
        self._thread = QThread()
        self._renamer = Renamer(
            files=tuple(self._files),
            prefix=prefix,
        )
        self._renamer.moveToThread(self._thread)
        # Rename
        self._thread.started.connect(self._renamer.renameFiles)
        # Update state
        self._renamer.renamedFile.connect(self._updateStateWhenFileRenamed)
        self._renamer.progressed.connect(self._updateProgressBar)
        self._renamer.finished.connect(self._updateStateWhenNoFiles)
        # Clean up
        self._renamer.finished.connect(self._thread.quit)
        self._renamer.finished.connect(self._renamer.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()

    def _updateStateWhenFileRenamed(self, newFile):
        self._files.popleft()
        self.srcFileList.takeItem(0)
        self.dstFileList.addItem(str(newFile))

    def _updateProgressBar(self, fileNumber):
        progressPercent = int(fileNumber / self._filesCount * 100)
        self.progressBar.setValue(progressPercent)