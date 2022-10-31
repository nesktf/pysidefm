from PySide2.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QFrame,
    QScrollArea,
    QGroupBox,
    QMenu,
    QMessageBox,
    QTextEdit
)

from PySide2.QtCore import Qt
from PySide2 import QtGui

from fileCls import FileNode


class MainWindow(QMainWindow):
    """Widget ventana principal"""
    # ==== Clases Internas ===== #
    class ButtCont(QFrame):
        def __init__(self, parent):
            super().__init__(parent=parent)
            self.layout = QHBoxLayout(self)

        def addWidget(self, widget):
            self.layout.addWidget(widget)

    class PathEditor(QFrame):
        def __init__(self, parent):
            super().__init__(parent=parent)
            self.parent = parent
            self.setMinimumHeight(35)
            self.setMaximumHeight(35)
            self.layout = QHBoxLayout(self)
            self.layout.setContentsMargins(5, 5, 5, 5)

            self.label = QLabel(parent.currFolder.getPath())
            self.layout.addWidget(self.label)

            self.pathbox = QTextEdit(self)
            self.pathbox.hide()
            self.pathbox.setMaximumHeight(40)
            self.pathbox.setText(parent.currFolder.getPath())
            self.pathbox.focusOutEvent = lambda event: self.pathUnfocus()
            self.layout.addWidget(self.pathbox)

            self.gobutt = QPushButton(">", self)
            self.gobutt.hide()
            self.gobutt.setMaximumHeight(40)
            self.gobutt.clicked.connect(lambda: self.changeFolder())
            self.gobutt.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.layout.addWidget(self.gobutt)

            self.setObjectName("PathEditor")
            self.setStyleSheet("QFrame#PathEditor{border: 1px solid black}")
        
        def mousePressEvent(self, QMouseEvent):
            if (QMouseEvent.button() == Qt.LeftButton):
                self.pathbox.show()
                self.pathbox.setFocus()
                self.pathbox.moveCursor(QtGui.QTextCursor.End)
                self.gobutt.show()
                self.label.hide()

        def pathUnfocus(self):
            self.pathbox.hide()
            self.gobutt.hide()
            self.label.show()

        def update(self):
            self.label.setText(self.parent.currFolder.getPath())
            self.pathbox.setText(self.parent.currFolder.getPath())

        def changeFolder(self):
            if (self.parent.currFolder.getPath() != self.pathbox.toPlainText()):
                try:
                    self.parent.appendFolder(FileNode(path=self.pathbox.toPlainText(), populate=True))
                except FileNotFoundError:
                    menu = QMessageBox()
                    menu.warning(self, '', "Ruta inválida")
                    self.pathbox.setText(self.label.text())
            self.pathUnfocus()

    # ===== Constructores ===== #
    def __init__(self, initFolder):
        super().__init__(parent=None)
        self.folderList = []
        self.index = 0
        self.folderList.append(FileNode(path = initFolder, populate = True))
        self.currFolder = self.folderList[self.index]

        self.setWindowTitle("PyQTFileBrowser")
        self.resize(800, 600)

        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout.setContentsMargins(5, 5, 5, 5)

        self.__initWidgets()

    def __initWidgets(self):
        self.pathEditor = self.PathEditor(self)
        self.centralLayout.addWidget(self.pathEditor)

        self.buttCont = self.ButtCont(self)
        self.centralLayout.addWidget(self.buttCont)

        self.backButt = QPushButton("<", self)
        self.backButt.clicked.connect(lambda: self.back())
        self.backButt.setDisabled(True)
        self.backButt.setMaximumWidth(40)
        self.buttCont.addWidget(self.backButt)

        self.nextButt = QPushButton(">", self)
        self.nextButt.clicked.connect(lambda: self.next())
        self.nextButt.setDisabled(True)
        self.nextButt.setMaximumWidth(40)
        self.buttCont.addWidget(self.nextButt)

        upButt = QPushButton("Carpeta superior", self)
        upButt.clicked.connect(lambda: self.appendFolder(FileNode.genParent(self.currFolder)))
        self.buttCont.addWidget(upButt)

        
        self.folderContent = FolderContent(self, self.currFolder)
        self.centralLayout.addWidget(self.folderContent)
    
    # ===== Manejo de Widgets ===== #
    def updateContent(self):
        self.folderContent.deleteLater()
        self.folderContent = FolderContent(self, self.currFolder)
        self.pathEditor.update()
        self.centralLayout.addWidget(self.folderContent)

    def appendFolder(self, folder):
        for i in range(self.index+1, len(self.folderList)):
            self.folderList.pop(-1)
        self.folderList.append(folder)
        self.index += 1
        self.currFolder = self.folderList[self.index]
        self.backButt.setDisabled(False)
        self.nextButt.setDisabled(True)
        self.updateContent()

    def back(self):
        self.index -= 1
        self.currFolder = self.folderList[self.index]
        self.nextButt.setDisabled(False)
        if (self.index == 0):
            self.backButt.setDisabled(True)
        self.updateContent()

    def next(self):
        self.index += 1
        self.currFolder = self.folderList[self.index]
        if (self.index != 0):
            self.backButt.setDisabled(False)
        if (self.index == len(self.folderList)-1):
            self.nextButt.setDisabled(True)
        self.updateContent()

class FolderContent(QFrame):
    """Widget contenido de carpeta"""
    # ===== Clases Internas ===== #
    class Item(QFrame):
        def __init__(self, parent, item):
            super().__init__(parent=parent)
            self.layout = QVBoxLayout(self)
            self.setObjectName("Item")
            self.setStyleSheet("QFrame#Item{border: 1px solid white;} QFrame#Item:hover{border: 1px solid red;}")
            self.setMaximumHeight(200)
            self.__item = item
            if (item.isFolder()):
                self.layout.addWidget(QLabel(item.getName()+"/"))
            else:
                self.layout.addWidget(QLabel(item.getName()))

        def mousePressEvent(self, QMouseEvent):
            if (QMouseEvent.button() == Qt.LeftButton):
                self.leftClickEvent(QMouseEvent)
            elif (QMouseEvent.button() == Qt.RightButton):
                self.rightClickEvent()

        def contextMenuEvent(self, event):
            menu = QMenu(self)
            delOpt = menu.addAction("Borrar")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if (action == delOpt):
                askstr = "¿Quieres borrar \""+self.__item.getName()+"\""
                if (self.__item.isFolder()):
                    askstr += "\nSe borrará la carpeta y todas sus subcarpetas"
                delmenu = QMessageBox()
                delmenu.question(self, '', askstr, delmenu.Yes, delmenu.No)
                if (delmenu.Yes):
                    self.__item.getParent().delChild(self.__item.getName(), delFile=True)
                    self.deleteLater()
            
        def rightClickEvent(self):
            pass
        
        def leftClickEvent(self):
            pass

    # ===== Constructores ===== #
    def __init__(self, parent, folder):
        super().__init__(parent=parent)
        self.currFolder = folder
        self.window = parent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.content = QGroupBox(self)
        self.content.setObjectName("FolderContent")
        self.content.setStyleSheet("QFrame#FolderContent{border: 1px solid black}")
        self.contLayout = QFormLayout(self.content)
        self.contLayout.setContentsMargins(5, 5, 5, 5)

        scroll = QScrollArea()
        scroll.setWidget(self.content)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.setStyleSheet("QFrame#FolderContent{border: 1px solid black}")
        self.__initWidgets()

    def __initWidgets(self):
        for i in self.currFolder.getFolderChildren():
            self.pushFile(i)
        for i in self.currFolder.getFileChildren():
            self.pushFile(i)

    # ===== Manejo de Widgets ===== #
    def pushFile(self, file):
        fileItem = self.Item(self, file)
        fileItem.leftClickEvent = lambda event: self.leftClickEvent(file)
        
        self.contLayout.addWidget(fileItem)

    # ===== Eventos ===== #
    def leftClickEvent(self, file):
        if (file.isFolder()):
            if (not file.isPopulated()):
                file.populate()
            self.window.appendFolder(self.window.currFolder.getChild(file.getName()))
