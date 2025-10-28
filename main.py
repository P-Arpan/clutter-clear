#clear the clutter
import os
from os import DirEntry


def Check_path(directory_path: str) -> None:
    """Directory checker function

    To access any path it must exist and required permissions must be available. This function checks path's existence and are the permissions available.

    Args:
        directory_path: Target Directory path
    Prints:
        Confirmation, if path passes all the checks.
    Raises:
        FileNotFoundError("DirectoryNotFoundError")
        PermissionError("DirectoryNotReadableError")
        PermissionError("DirectoryNotWritableError")

    Note: Originally returned bool, but realized validators should use exceptions for control flow (EAFP pattern). - 2025-10-28
    """
    if os.access(directory_path, os.F_OK):
        if not os.access(directory_path, os.R_OK):
            #TODO: add logging here (f"{directory_path} accessible but not readable")
            raise PermissionError("DirectoryNotReadableError")
        
        elif not os.access(directory_path, os.W_OK):
            #TODO: add logging here (f"{directory_path} accessible and readable but not writable")
            raise PermissionError("DirectoryNotWritableError")

        else:
            print(f"Using Directory: '{directory_path}'")
    else:
        #print("Directory Inaccessible")
        raise FileNotFoundError("DirectoryNotFoundError")   

def process_files(file_extension: str, directory_path: str) -> None:
    """File processor function.

    To get entries in a directory, we need to scan it.
    Check if the entries are of the required file_extension
    and further we rename the entries which pass the checks

    The file_counter is used to keep track of the files renamed.
    displays a confirmation message for each file renamed[for better UX]

    Args:
        file_extension: Target File Extension
        directory_path: Target Directory path
    Prints:
        1. No file found msg, when file_counter==0
        2. Confirms all file renamed

    Caution:
        Modifies files on disk
    """
    with os.scandir(directory_path) as dir_entries:
        print(f"Scanning '{directory_path}'...")
        file_number=0        #Counter for file name[According to number of target files in directory_path]
        for entry in dir_entries:    
            if entry.is_file():
                if (not entry.name.startswith(".")) and entry.name.endswith(f".{file_extension}"):
                    #is hidden file? and is required type?
                    file_number+=1
                    file_number, msg=renamer(directory_path, file_extension, entry, file_number)
                    print(msg)          #printing confirmation of renaming procedure

        if file_number!=0:
            print (f"All '.{file_extension}' files in '{directory_path}' renamed.")
        else:
            print(f"No file of type '.{file_extension}' found in '{directory_path}'")

def renamer(directory_path: str, file_extension: str, current_file_entry: DirEntry, file_number: int) -> tuple[int,str]:
    """File renamer function

    Generating names. renaming using rename() instead of replace(), since replace overrides the old file when name conflict is encountered.

    Args:
        directory_path: Target Directory Path
        file_extension: Target File Extension
        current_file_entry: DirEntry object from DirEntry iterable[here it accepts entry in process_files()]
        file_number: Counter for file name[According to number of target files in directory_path]
    Returns:
        updated file_number and confirmation msg 
    
    Caution:
        Modifies files on disk
    """
    newpath, file_number=generate_name(directory_path, file_extension, file_number)
    os.rename(current_file_entry.path, newpath)
    #returning file_number so that further are also produced serially
    return (file_number, f"{current_file_entry.name} --> {os.path.basename(newpath)}") 

def generate_name(directory_path: str, file_extension: str, file_number: int) -> tuple[str,int]:
    """The name generator function.

    Since name conflict can arise, function checks is there already existing file of newname. When there is, file_number is updated to create a newname which must not create conflict

    Args:
        directory_path: Target Directory
        file_extension: Target File Extension
        file_number: Counter for file name[According to number of target files in directory_path]
    Returns:
        newpath and updated file_number
    """
    while True:
        newname=f"{file_number}.{file_extension}"
        newpath=os.path.join(directory_path,newname)
        if not os.path.exists(newpath):
            return newpath,file_number  #file_number so that further names are serially after current file_number
        file_number+=1

def path_cleaner(directory_path:str)->str:
    """The directory path cleaner function.

    Windows Explorer wraps paths with spaces in quotes when copying.
    This breaks os.path operations, so we strip them.

    Args:
    directory_path: Target Directory Path
    Returns:
        new directory_path stripped of quotes
    """
    if directory_path[-1]=="'" and directory_path[0]=="'":
        return directory_path.strip("'")
    elif directory_path[-1]=='"' and directory_path[0]=='"':
        return directory_path.strip('"')
    else:
        return directory_path

def run() -> None:
    """The initiator function.

    Starts the Clutter Clearer. And takes required input from user
    
    Accepts FileNotFoundError and PermissionError"""

    directory_path,file_extension="<Not Set>","<Not Set>"
    try:
        print("-----CLUTTER CLEARER INITIALISED-----")
        print("\n")

        print("Current Path:",os.getcwd())
        directory_path=path_cleaner(input("Enter absolute path for target directory:")) 
        #directory_path: Target Directory Path
        Check_path(directory_path)
        file_extension=input("Enter File Extension of files to rename:").lower()
        print("\n")
        #file_extension: Target File Type Extension
        process_files(file_extension,directory_path)

    except FileNotFoundError as F_err:
        print(f"Directory: '{directory_path}' not found.\nDetails:\n{F_err}")
        print(f"Please reenter the directory and try again.")

    except PermissionError as Perm_err:
        print(f"Permission not available for directory: '{directory_path}'\nDetails:\n{Perm_err}")
        print(f"You may need to provide permission.")
    
    finally:
        pass
        #add code to restrat program


if __name__=="__main__":
   run()
