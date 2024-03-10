from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from .ui.window import Ui_Window
from .ui.removeDialog import Ui_removeDialog
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
        self.setWindowIcon(QtGui.QIcon("Bulkrr_Logo.jpg"))

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
        self.editFileQueueButton.setEnabled(False)
        self.clearFileQueueButton.setEnabled(False)
        self.loadFilesButton.setText("Load Files")
        self.prefixEdit.clear()

    def _updateStateWhenFilesLoaded(self):
        self.prefixEdit.setEnabled(True)
        self.prefixEdit.setFocus(True)
        self.loadFilesButton.setText("Load More Files")
        self.clearFileQueueButton.setEnabled(True)
        self.editFileQueueButton.setEnabled(True)

    def _updateStateWhenReady(self):
        if self.prefixEdit.text():
            self.renameFilesButton.setEnabled(True)
            self.loadFilesButton.setText("Load More Files")
        else:
            self.renameFilesButton.setEnabled(False)

    def _updateStateWhileRenaming(self):
        self.loadFilesButton.setEnabled(False)
        self.renameFilesButton.setEnabled(False)
        self.editFileQueueButton.setEnabled(False)
        self.clearFileQueueButton.setEnabled(False)
        self.prefixEdit.setEnabled(False)
    
    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
        self.renameFilesButton.clicked.connect(self.renameFiles)
        self.prefixEdit.textChanged.connect(self._updateStateWhenReady)
        self.prefixEdit.textEdited.connect(self._validatePrefixChars)
        self.prefixEdit.returnPressed.connect(self.renameFiles)
        self.editFileQueueButton.clicked.connect(self._removeItemsWindow)
        self.clearFileQueueButton.clicked.connect(self._clearFileQueue)

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

    def _validatePrefixChars(self):
        prefix = self.prefixEdit.text()
        invalidCharacters = '"\/:*?"<>|'
        for i in invalidCharacters:
            if i in prefix:
                self._spawnMessageBox(
                    "Invalid Prefix",
                    f"The prefix cannot contain the following characters: {invalidCharacters}"
                )
                self.prefixEdit.clear()
                self.prefixEdit.setFocus(True)
                break

    def _spawnMessageBox(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def _removeItemsWindow(self):
        self._removeDialog = RemoveDialog(self._files)
        self._removeDialog.setWindowIcon(QtGui.QIcon("Bulkrr_logo.jpeg"))
        self._removeDialog.changesSubmitted.connect(self._updateFilesQueue)
        self._removeDialog.show()

    def _updateFilesQueue(self):
            self._files = self._removeDialog.updatedFiles
            self._filesCount = len(self._files)
            self.srcFileList.clear()
            for file in self._files:
                self.srcFileList.addItem(str(file))

    def _clearFileQueue(self):
        self._files.clear()
        self._filesCount = len(self._files)
        self.srcFileList.clear()
        self._updateStateWhenNoFiles()

class RemoveDialog(QWidget, Ui_removeDialog):
    changesSubmitted = pyqtSignal()

    def __init__(self, files: deque = deque()):
        super().__init__()
        self.files = files
        self.toRemove = []
        self.updatedFiles = files.copy()
        self._setupUI()

    def _setupUI(self):
        self.setupUi(self)
        for file in self.files:
            self.fileList.addItem(str(file))

    def accept(self):
        self.toRemove = self.fileList.selectedItems()
        for i in self.toRemove:
            self.updatedFiles.remove(Path(i.text()))
        self.changesSubmitted.emit()
        self.close()
    
    def reject(self):
        self.close()