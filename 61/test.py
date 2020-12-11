import os

path = '/home/w61/PatternRecognition/Fire_dataset'
filelist = os.listdir(path)
for files in filelist:
    files_path = os.path.join(path,files)
    print(files_path)