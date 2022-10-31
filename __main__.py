#!/usr/bin/env python
import gui
import os
import sys
from PySide2.QtWidgets import(QApplication)

def initGui():
    app = QApplication([])
    app.setApplicationName("PyQTFileBrowser")
    window = gui.MainWindow(os.getcwd())
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    initGui()
