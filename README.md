This program is used to separate **'images having texts'** from **'images without texts'** using an ocr ml model.\
*Only works if the texts are in english, for now*

## To make this work in your machine
1. Download python
(Before doing next step, creating a virtual environment might help you keep your system clean )
2.  For GPU users:
   `python
      pip install -r requirements-GPU.txt`\
    For CPU users:
   `python
      pip install -r requirements.txt`

{If you have GPU, then you also need to setup cuda, cuDNN seperately.
This [repo](https://github.com/entbappy/Setup-NVIDIA-GPU-for-Deep-Learning.git) might be helpfull}

3. Now run **'Text_Image_Separator.py'** file
4. Copy absolute path of the directory containing images you want to separate, by right-clicking on it and selecting the copy path option.
5. The images containing Text will be moved to *'Text'* sub-folder\
 & Images which script is not sure about will be moved to *'Unconfirmed'* sub-folder.\
[full path will be shown in confirmation message]

> [!CAUTION]
> 1. The directory MUST NOT have anything other than IMAGE FILES, OTHERWISE PROGRAM BREAKS
> 2. Script must have permissions to access, edit the directory.
> 3. IS NOT 100% ACCURATE!
