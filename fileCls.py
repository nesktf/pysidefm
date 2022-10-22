import os
import magic

class Node():
    """Clase Nodo (Para clase Folder)"""
    def __init__(self, path=None, content=None, parentTree = None):
        self.__parent = parentTree  # Árbol padre

        if (path == None and content == None):
            raise Exception("Path/Content not set")

        if (not path == None):
            if (not os.path.isfile(path)):
                self.__content = Folder(path, parentNode=self)
                self.__folder = True
            else:
                self.__content = File(path, parentNode=self)
                self.__folder = False

        if (not content == None):
            self.__content = content
            self.__folder = isinstance(content, Folder)
    
    # ====================== #

    def setParent(self, parent):
        """Setear nodo padre"""
        self.__parent = parent

    def getParentTree(self):
        """Devuelve árbol padre"""
        return self.__parent.getContent()

    # ====================== #

    def isFolder(self):
        """Devuelve tipo de nodo"""
        return self.__folder

    def getParent(self):
        """Devuelve el árbol padre"""
        return self.__parent

    def getContent(self):
        """Devuelve el contenido"""
        return self.__content

    # ====================== #


class File():
    """Clase archivo"""
    def __init__(self, filePath, parentNode = None):
        self.__path = filePath                  # Ruta/Path del archivo
        self.__type = magic.from_file(filePath) # Tipo del archivo
        self.__parent = parentNode

    def __str__(self): # Print string
        return self.getName()

    # ====================== #

    def setParent(self, parent):
        """Setear el nodo padre"""
        self.__parent = parent

    # ====================== #

    def getPath(self):
        """Devuelve la ruta/path al archivo"""
        return self.__path
    
    def getName(self):
        """Devuelve nombre de archivo"""
        return os.path.split(self.__path)[-1]
    
    def getType(self):
        """Devuelve tipo de archivo"""
        return self.__type

    def getParentTree(self):
        """Devuelve árbol padre"""
        return self.__parent.getParent()

    # ====================== #

class Folder():
    """Clase carpeta (Árbol de nodos)"""
    def __init__(self, folderPath, populate = False, parentNode = None):
        self.__path = folderPath    # Ruta de la carpeta
        self.__nodes = []           # Nodos de la carpeta
        self.__parent = parentNode
        self.__populated = populate

        if (populate):
            self.populate()

    def __str__(self):
        return self.getName()

    # ====================== #

    def printContents(self):
        if (self.isPopulated()):
            print("Path: "+self.__path)
            print("=> Folders:")
            for i in self.getFolders():
                print(str(i)+"/")
            print("=> Files:") 
            for i in self.getFiles():
                print(i)
        else:
            print("Folder not populated")


    def populate(self):
        """Inicializar el árbol"""
        self.__populated = True
        dirs = os.listdir(self.__path)
        for i in dirs:
            if (not self.hasFile(i)):
                self.__nodes.append(Node(
                    path=os.path.join(self.__path, i),
                    parentTree=self
                ))

    def setParent(self, parent):
        """Setear el nodo padre"""
        self.__parent = parent

    def pushNode(self, node):
        """Añadir nodo al árbol"""
        node.setParent(self)
        self.__nodes.append(node)

    # ====================== #

    def isPopulated(self):
        return self.__populated

    def getPath(self):
        """Devuelve la ruta/path a la carpeta"""
        return self.__path

    def getName(self):
        """Devuelve el nombre de la carpeta"""
        return os.path.split(self.__path)[-1]

    def getParentTree(self):
        """Devuelve el árbol padre"""
        return self.__parent.getParent()

    def hasFile(self, name):
        """Verificar si el árbol (inicializado) tiene cierto archivo/carpeta"""
        flag = False
        for i in self.__nodes:
            if (i.getContent().getName() == name):
                flag = True
                break
        return flag

    def getParentPath(self):
        """Devuelve path de la carpeta padre"""
        return os.path.abspath(os.path.join(self.__path, os.pardir))

    def getFolders(self):
        """Devuelve carpetas del árbol (objeto Folder)"""
        list = []
        for i in self.__nodes:
            if (i.isFolder()):
                list.append(i.getContent())
        return list

    def getFiles(self):
        """Devuelve archivos del árbol (objeto File)"""
        list = []
        for i in self.__nodes:
            if (not i.isFolder()):
                list.append(i.getContent())
        return list

    def get(self, name):
        """Devuelve archivo por nombre"""
        item = None
        for i in self.__nodes:
            if (i.getContent().getName() == name):
                item = i.getContent()
                break

        if (item == None):
            raise FileNotFoundError("Archivo no encontrado: "+name)
        
        return item

    # ====================== #

    @staticmethod
    def genParent(folder):
        parFolder = Folder(folderPath=folder.getParentPath())
        parFolder.pushNode(Node(content=folder))
        parFolder.populate()
        return parFolder

    # ====================== #

