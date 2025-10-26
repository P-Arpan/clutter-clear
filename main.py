#clear the clutter
import os


def Check_Set_path(Dpath)->None:
    """Dpath-> Directory to change
     \nChecks directory is accessible or not:
        \n  True->chdir Dpath & return True \n  raise DirectoryNotFoundError
        
        \n  if True but not updated to Dpath:
            return False"""
    
    if os.access(Dpath,os.F_OK)==False:       
        # print("Directory Inaccessible")
        raise FileNotFoundError("DirectoryNotFoundError")
    else:
        old=os.getcwd()
        os.chdir(Dpath)   #change directory to Dpath
        if os.getcwd()!=old:
            print(f"Directory Updated to {Dpath}")
            return True
        else:
            print(f"Directory not updated.\n Current directory: {os.getcwd()}")
            return False

def files(Ftype:str,Dpath:str)->None:
    """Ftype-> File Type to change 
    \nDpath-> Directory to change"""
    with os.scandir() as DirEntires:
        files.File_no=0               #file name counter
        for file in DirEntires:    

            if file.is_file():
                if (not file.name.startswith(".")) and file.name.endswith(f".{Ftype}"):
                    #hidden file? and reqired type?

                    files.File_no+=1     
                    newname=f"{str(files.File_no)}.{Ftype}"
                    
                    frenamed=renamed(file,newname,Ftype)
                    print(frenamed) #printing renamed confirmation
        if files.File_no!=0:
            print (f"All {Ftype} files in {Dpath} renamed.")
        else:
            print(f"No file of type {Ftype} found in \n{Dpath}")

def renamed(file,newname: str,Ftype: str)->str:
    """file-> DirEntry object
    \nnewname->New generated name using counter
    \nFtype-> File Type to change
    
    \nChecking does name exist:
    \n  if True: generate new name
    \n  if False: rename and return confirmation string"""
    if not os.path.exists(newname):
        os.rename(file.name,newname)   #since file name does not exist renaming           
        return f"{file.name} --> {newname}" #return confirmation
    else:
        files.File_no+=1
        newname=f"{str(files.File_no)}.{Ftype}"
        return renamed(file,newname,Ftype) 
        
    """if you dont return then when ever name conflict arises, name will get changed but function will return NONE!"""
   
def run():
    """Dpath-> Directory Path , Ftype-> File Type Extension"""
    try:
        print("-----CLUTTER CLEARER INITIALISED-----")
        print("Current Path:",os.getcwd())
        Dpath=input("Enter directory path:")
        if Check_Set_path(Dpath):
            Ftype=input("Enter File Extension of files to rename:")
            files(Ftype,Dpath)
        else:
            if not os.access(Dpath,os.R_OK):
                print("{Dpath} accessible but not readable")
            else:
                if not os.access(Dpath,os.W_OK):
                    print("{Dpath} accessible and readable but not writable")

    except FileNotFoundError:
        print(f"Directory:\n{Dpath}\n not found.\nPlease restart the application and try again")
    finally:
        pass
        #add code to restrat program


#test
run()
