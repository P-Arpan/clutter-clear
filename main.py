'''Q. Use os module to-->
Rename files inside a folder as "1" to "n","n" is "total no. of files inside".
take "file format" as argument'''

import os


class Rename:
    def __init__(self,Dpath:str,Ftype:str):
        """Dpath-> Directory Path , Ftype-> File Type Extension"""

        self.Dpath=Dpath
        self.Ftype=Ftype.lower()
        self.Check_Set_Path(Dpath) #checking if path is accesible.
    
    def Check_Set_Path(self,path):
        """Checks directory is accessible or not.
        \nTrue->set path 
        \nFalse->print 'Directory Inaccessible'"""

        if os.access(path,os.F_OK)==False:       
            print("Directory Inaccessible")
            exit()
        else: 
            os.chdir(path)                #change directory to Dpath
            if os.getcwd()==path:
                print(f"Directory Updated to {path}")
            else:
                print(f"Directory not updated.\n Current directory: {os.getcwd()}")

    def Files(self):
        with os.scandir(self.Dpath) as DirEntires:

            self.File_no=0                      #initialising file name counter
            for self.entry in DirEntires:       #iterating files in scandir iterable

                if (not self.entry.name.startswith(".")) and self.entry.is_file() and self.entry.name.endswith(f".{self.Ftype}"):      
                    #checking whether entry is hidden, file, and File type
                    
                    self.File_no+=1    #increasing file name counter       
                    newname=f"{str(self.File_no)}.{self.Ftype}"
                    
                    temp=self.renamed(newname)
                    print(temp)
                    
                    
                    
            if self.File_no!=0:
                print (f"All {self.Ftype} files in {self.Dpath} renamed.")
            else:
                print(f"No file of type {self.Ftype} found in \n{self.Dpath}")

    def renamed(self,newname: str)->str:
        """Checks if file name already exists.
        \n if true then produces new file name"""
        if not os.path.exists(newname):
            os.rename(self.entry.name,newname)              
            return f"{self.entry.name} --> {newname}"
        else:
            self.File_no+=1
            newname=f"{str(self.File_no)}.{self.Ftype}"
            return self.renamed(newname) 
        
        """if you dont return then when ever name conflict arises, name will get changed but fucntion will return NONE!"""

if __name__=="__main__":
    print("-----CLUTTER CLEARER INITIALISED-----")

    Dir=input("Enter directory path:")
    ext=input("Enter File Extension of files to rename:")

    test=Rename(Dir,ext)
    test.Files()


