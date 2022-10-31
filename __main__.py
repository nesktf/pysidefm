import gui
import os
import sys
from PySide2.QtWidgets import(QApplication)
from fileCls import FileNode

def main():
    node = FileNode(os.getcwd(), populate=True)
    parent = FileNode.genParent(node)
    parent.printChildren()

    parent.getChild("proyecto").printChildren()

def initGui():
    app = QApplication([])
    app.setApplicationName("PyQTFileBrowser")
    window = gui.MainWindow(os.getcwd())
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    #main()
    initGui()
