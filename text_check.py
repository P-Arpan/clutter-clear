import easyocr
ocr=easyocr.Reader(lang_list=['en'],model_storage_directory="ocr_models")
#d.__doc__
#print("\n",[i for i in ocr.__dir__()])
#recogtext=ocr.readtext(r"D:\1-CS\Practice_Proj\clutter clear\change\Screenshot 2025-10-15 214510.png")
def r(recogtext):
    for j in recogtext:
        if j[2]>0.50:
            print(f"Text: '{j[1]}' ---- Confidence: {int(j[2]*100)} %")
        #TODO: make a counter of confidence percentage if 5 or 6 is greter than a certain value then it should be called that it has text
        else:
            print("image has no text")

def extract(img_path: str)-> list:
    recognised=ocr.readtext(img_path)
    return recognised

def check(recognised)->int:
    """RETURNS:
    veryconfident-> 1
    underconfident-> 0
    neither-> 2"""
    underconfident=0
    veryconfident=0
    for ele in recognised:
        if ele[2]<0.60:
            underconfident+=1
        elif ele[2]>0.80:
            veryconfident+=1
    
    if veryconfident>0:
        return 1
    elif underconfident>0:
        return 0
    else:
        return 2


if __name__=="__main__":
    ck=check(extract(r"change\1.png"))
    print(ck)