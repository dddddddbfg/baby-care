import os

def GetFileList(FindPath, FlagStr=[]):
    fileList = []
    FileNames = os.listdir(FindPath)
    if len(FileNames)>0:
        print (len(FileNames))
        for fn in FileNames:
            fullname = os.path.join(FindPath,fn)
            if 'AN' in fullname:
                print (fullname+' Angry')
                fileList.append(fullname+' '+'0')
            if 'DI' in fullname:
                print (fullname+' Disgust')
                fileList.append(fullname+' '+'1')
            if 'FE' in fullname:
                print (fullname+' Fear')
                fileList.append(fullname+' '+'2')
            if 'HA' in fullname:
                print (fullname+' Happy')
                fileList.append(fullname+' '+'3')
            if 'NE' in fullname:
                print (fullname+' Neutral')
                fileList.append(fullname+' '+'4')
            if 'SA' in fullname:
                print (fullname+' Sad')
                fileList.append(fullname+' '+'5')
            if 'SU' in fullname:
                print (fullname+' Surprise')
                fileList.append(fullname+' '+'6')
    # fileList.sort()
    return fileList

images = GetFileList('./')
train_txt = open('train.txt','w')
for img in images:
    str1 = img +'\n'
    train_txt.writelines(str1)

images = GetFileList('./')
val_txt = open('val.txt','w')
for img in images:
    str1 = img +'\n'
    val_txt.writelines(str1)
