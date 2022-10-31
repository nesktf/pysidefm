import os
import platform
import shutil

# Windows necesita python-magic-win64 en vez de python-magic
if (platform.system() == "Windows"):
    from winmagic import magic
else:
    import magic

class FileNode():
    """Nodo archivo/carpeta"""
    # ===== Constructores ===== #
    def __init__(self, path, parent = None, populate = False):
        self.__path = path
        self.__parent = parent
        self.__type = None

        self.__isFolder = os.path.isdir(path)
        if (self.__isFolder):
            self.__folderInit(populate)
        else:
            self.__fileInit()

    def __folderInit(self, populate):
        self.__children = []
        self.__type = "folder"

        if (populate):
            self.populate()

    def __fileInit(self):
        try:
            self.__type = magic.from_file(self.__path)
        except PermissionError:
            # A veces no se puede conseguir el tipo de archivo por falta de permisos
            # se usa la extensión como tipo de archivo en ese caso
            self.__type = self.__path.split(".")[-1]

    # ===== Manejo de nodos ===== #
    def populate(self):
        """Parsear los nodos de una carpeta"""
        if (self.__isFolder):
            dirs = os.listdir(self.__path)
            for i in dirs:
                try:
                    self.__children.append(FileNode(path = os.path.join(self.__path, i), parent = self))
                except FileNotFoundError:
                    # A veces hay symlinks rotos
                    print("Invalid file: "+i)
        else:
            raise NotADirectoryError

    def printChildren(self):
        """Printear los nodos"""
        if (self.__isFolder):
            print(self.__path)
            print("=> Folders:")
            for i in self.getFolderChildren():
                print(i.getName()+"/")
            print("=> Files:")
            for i in self.getFileChildren():
                print(i.getName())
        else:
            raise NotADirectoryError

    def replChild(self, newChild):
        """Reemplazar un nodo"""
        flag = False
        for i in range(len(self.__children)):
            if (self.__children[i].getName() == newChild.getName()):
                self.__children[i] = newChild
                flag = True
                break
        if (not flag):
            raise FileNotFoundError

    def delChild(self, name, delFile=False):
        """Eliminar un nodo por nombre"""
        flag = False
        for i in range(len(self.__children)):
            if (self.__children[i].getName() == name):
                flag = True
                if (delFile):
                    print("remove: "+self.__children[i].getPath())
                    if (self.__children[i].isFolder()):
                        #TODO: Solo borra carpetas vacias, cambiar por shutil para borrar recursivamente
                        os.rmdir(self.__children[i].getPath())
                    else:
                        os.remove(self.__children[i].getPath())
                self.__children.pop(i)
                break

        if (not flag):
            raise FileNotFoundError

    # ===== Getters Booleanos ===== #
    def isFolder(self):
        """Es carpeta"""
        return self.__isFolder

    def hasChild(self, name):
        """Buscar nodo por nombre"""
        flag = False
        if (self.__isFolder):
            for i in self.__children:
                if (i.getName() == name):
                    flag = True
                    break
        else:
            raise NotADirectoryError
        return flag

    def isPopulated(self):
        """Está populado"""
        if (self.__isFolder):
            return (not len(self.__children) == 0)
        else:
            raise NotADirectoryError

    # ===== Getters ===== #
    def __str__(self): # Para printear nodos
        return self.getName()

    def getPath(self):
        """Path"""
        return self.__path
    
    def getType(self):
        """Tipo de nodo"""
        return self.__type

    def getName(self):
        """Nombre del archivo/carpeta"""
        return os.path.split(self.__path)[-1]

    def getParent(self):
        """Nodo padre"""
        return self.__parent

    def getParentPath(self):
        """Path del nodo padre"""
        if (self.__parent == None):
            return os.path.abspath(os.path.join(self.__path, os.pardir))
        else:
            return self.__parent.getPath()

    def getFolderChildren(self):
        """Listar todos los nodos hijos que son carpetas"""
        list = []
        if (self.__isFolder):
            for i in self.__children:
                if (i.isFolder()):
                    list.append(i)
        else:
            raise NotADirectoryError
        return list
    
    def getFileChildren(self):
        """Listar todos los nodos hijos que son archivos"""
        list = []
        if (self.__isFolder):
            for i in self.__children:
                if (not i.isFolder()):
                    list.append(i)
        else:
            raise NotADirectoryError
        return list
        
    def getChild(self, name):
        """Nodo por nombre"""
        child = None
        if (self.__isFolder):
            for i in self.__children:
                if (i.getName() == name):
                   child = i
                   break
        else:
            raise NotADirectoryError
        return child

    # ===== Funciones estáticas ===== #
    @staticmethod
    def genParent(fileNode):
        """Generar nodo padre a partir de otro nodo"""
        parFolder = FileNode(path=fileNode.getParentPath(), populate=True)
        parFolder.replChild(fileNode)
        return parFolder

