import fileCls
import os

def main():
    folder = fileCls.Folder(folderPath=os.getcwd(), populate=True)
    folder.get(".git").populate()
    folder = fileCls.Folder.genParent(folder)

    folder.printContents()
    print("")
    folder.get("proyecto").printContents()
    print("")
    folder.get("proyecto").get(".git").printContents()
    print("")
    folder.get("proyecto").get(".git").getParentTree().printContents()

if __name__ == "__main__":
    main()
