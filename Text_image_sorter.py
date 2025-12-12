#clear the clutter start date:20-10-25
import os
import easyocr

ocr=easyocr.Reader(lang_list=['en'],gpu=True,model_storage_directory=r"ocr_models",download_enabled=False)

def extract(img_path: str)-> list:
    """setup readtext()"""
    recognised=ocr.readtext(img_path)
    return recognised

def check(recognised)->int:
    """RETURNS: veryconfident-> 1  underconfident-> 0  neither-> 2"""
    underconfident,veryconfident=0,0
    for ele in recognised:
        if ele[2]<0.60: underconfident+=1
        elif ele[2]>0.80:   veryconfident+=1
    if veryconfident>0: return 1
    elif underconfident>0:  return 0
    else:   return 2

def Check_path(directory_path: str) -> None:
    """Raises:
    \nFileNotFoundError("DirectoryNotFoundError")
    \nPermissionError("DirectoryNotReadableError")
    \nPermissionError("DirectoryNotWritableError")
    """
    if os.access(directory_path, os.F_OK):
        if not os.access(directory_path, os.R_OK):
            #TODO: add logging here (f"{directory_path} accessible but not readable")
            raise PermissionError("DirectoryNotReadableError")
        elif not os.access(directory_path, os.W_OK):
            #TODO: add logging here (f"{directory_path} accessible and readable but not writable")
            raise PermissionError("DirectoryNotWritableError")
        else:
            print(f"Using Directory: '{directory_path}\'")
    else:
        raise FileNotFoundError("DirectoryNotFoundError")   

def move_files(directory_path: str) -> None:
    """
    Moves images containing text to 'Text' folder,
    and unconfimed or underconfident images to 'unconfirmed' folder
    Images not containing text stay in original directory 
    """
    with os.scandir(directory_path) as dir_entries:
        print(f"Scanning '{directory_path}\\'...")
        notxt_img=0
        txt_img=0               #images containg text counter
        unconfirmed_img=0       #images on which ocr is doubtful
        
        for entry in dir_entries:
            if entry.is_file() and (not entry.name.startswith(".")):
                if check(extract(entry.path))==1:           
                    text_path=directory_path+"\\Text\\"     #move text img to 'Text' folder
                    os.rename(entry.path,text_path+entry.name)                  
                    txt_img+=1
                    print(f"{entry.name} contains text")                             
                elif check(extract(entry.path))==2:
                    unconfirmed_path=directory_path+"\\Unconfirmed\\"   #move text img to 'Unconfimed'
                    os.rename(entry.path,unconfirmed_path+entry.name)
                    unconfirmed_img+=1
                    print(f"{entry.name} might contain text")
                else:
                    notxt_img+=1   
        if txt_img!=0:
            print (f"{txt_img} images containing text moved to {directory_path+"\\Text"}.")
            if unconfirmed_img!=0:
                print (f"{txt_img} images containing text moved to {directory_path+"\\Unconfirmed"}.")
        elif unconfirmed_img!=0:
                print (f"{txt_img} images containing text moved to {directory_path+"\\Unconfirmed"}.")
        elif notxt_img!=0:
            print(f"No image containing text found in '{directory_path}\\'")
        else:
            print(f"No image found in '{directory_path}\\'")

def path_cleaner(directory_path:str)->str:
    '''Returns: new directory_path stripped of quotes'''
    if directory_path[-1]=="'" and directory_path[0]=="'":
        return directory_path.strip("'")
    elif directory_path[-1]=='"' and directory_path[0]=='"':
        return directory_path.strip('"')
    else:
        return directory_path

def dir_creator(directory_path:str)->None:
    """Creates directory for images with images having text and unconfirmed images"""
    path_holder=os.getcwd()     #storing original path
    os.chdir(directory_path)
    if not os.path.exists(directory_path+"\\Text"):
        os.mkdir(directory_path+"\\Text") #creates a folder to store text
        print("Directory 'Text' created successfully")
    if not os.path.exists(directory_path+"\\Unconfirmed"):
        os.mkdir(directory_path+"\\Unconfirmed") #creates a folder to store text
        print("Directory 'Unconfirmed' created successfully")
    os.chdir(path_holder)       #coming back to original path

def run() -> None:
    directory_path="<Target Directory Path>"      
    restarted=1
    while restarted>0:
        try:
            if restarted==1:
                print("-----CLUTTER CLEARER INITIALISED-----")
            else:
                print("\n-----CLUTTER CLEARER RE-INITIALISED-----")        
            print("Current Path:",os.getcwd())
            directory_path=input("Enter absolute path for target directory:")
            
            if len(directory_path)==0:
                print("\nNo path provided. Please Try again.")
                print("To exit write 'exit' ")
                continue
            elif directory_path.lower()=="exit":
                exit()
            else:
                directory_path=path_cleaner(directory_path) 
                Check_path(directory_path)

            dir_creator(directory_path)
            move_files(directory_path)
            return        
        except FileNotFoundError as F_err:
            print(f"Directory: '{directory_path}' not found.\nDetails:\n{F_err}")
            print(f"Please check if you entered absolute path '{directory_path}'")
            print(f"Please reenter the directory and try again.")
        except PermissionError as Perm_err:
            print(f"Permission not available for directory: '{directory_path}'\nDetails:\n{Perm_err}")
            print(f"You may need to provide permission.")
        finally:
            restarted+=1 #keeping count of restarts
        
if __name__=="__main__":
    run()