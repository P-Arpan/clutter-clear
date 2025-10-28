#clear the clutter
import os
from os import DirEntry


def Check_Set_path(Dpath: str) -> None:
    """
    Dpath-> Target Directory
     
    Multi-Level checks of directory:
    Check Accessibility:T-> Readibility:T-> Writability:T-> Use Dpath

    \n Accessibility-False: DirectoryNotFoundError
    \n Readibility-False: DirectoryNotReadableError
    \n Writability-False: DirectoryNotWritableError

\nNote: Originally returned bool, but realized validators should
use exceptions for control flow (EAFP pattern). - 2025-10-28
    """
    if os.access(Dpath, os.F_OK):
        if not os.access(Dpath, os.R_OK):
            #print(f"{Dpath} accessible but not readable")
            raise PermissionError("DirectoryNotReadableError")
        elif not os.access(Dpath, os.W_OK):
            #print(f"{Dpath} accessible and readable but not writable")
            raise PermissionError("DirectoryNotWritableError")
        else:
            print(f"Using Directory: '{Dpath}'")
    else:
        #print("Directory Inaccessible")
        raise FileNotFoundError("DirectoryNotFoundError")   

def files(Ftype: str, Dpath: str) -> None:
    """Ftype-> Target File Extension
    \nDpath-> Target Directory
    
    \nScans Dpath and produces DirEntry iterable->
    Check is file with target extension->
    Rename file using renamer() function->print Confirmation msg

    \n if no file found: display msg 
    """

    with os.scandir(Dpath) as DirEntires:
        print(f"Scanning '{Dpath}'...")

        File_no=0        #counter for new file name acc. to total no of files
        for file in DirEntires:    
            if file.is_file():
                if (not file.name.startswith(".")) and file.name.endswith(f".{Ftype}"):
                    #hidden file? and reqired type?
                    File_no+=1
                    File_no, msg=renamer(Dpath, Ftype, file, File_no)
                    print(msg) #printing renamed confirmation

        if File_no!=0:
            print (f"All '.{Ftype}' files in '{Dpath}' renamed.")
        else:
            print(f"No file of type '.{Ftype}' found in '{Dpath}'")

def renamer(Dpath: str, Ftype: str, current_file: DirEntry, File_no: int) -> tuple[int,str]:
    
        newpath, File_no=generate_name(Dpath, Ftype, File_no)
        os.rename(current_file.path, newpath)
        return (File_no, f"{current_file.name} --> {os.path.basename(newpath)}") #return confirmation
        """if you dont return then when ever name conflict arises, name will get changed but function will return NONE!"""

def generate_name(Dpath: str, Ftype: str, File_no: int) -> tuple[str,int]:

    while True:
        newname=f"{File_no}.{Ftype}"
        newpath=os.path.join(Dpath,newname)
        if not os.path.exists(newpath):
            return newpath,File_no
        File_no+=1

def run() -> None:
    """The initiator and orcherstor function
    
    Dpath-> Directory Path , Ftype-> File Type Extension"""
    try:
        print("-----CLUTTER CLEARER INITIALISED-----")
        print("Current Path:",os.getcwd())
        Dpath=input("Enter complete directory path:")
        Check_Set_path(Dpath)
        Ftype=input("Enter File Extension of files to rename:").lower()
        files(Ftype,Dpath)

    except FileNotFoundError as F_err:
        print(f"Directory: '{Dpath}' not found.\nDetails:\n{F_err}")
        print(f"Please reenter the directory and try again.")

    except PermissionError as Perm_err:
        print(f"Permission not available for directory: '{Dpath}'\nDetails:\n{Perm_err}")
        print(f"You may need to provide permission.")

    finally:
        pass
        #add code to restrat program


if __name__=="__main__":
    run()
