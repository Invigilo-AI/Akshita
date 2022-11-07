# Downloader
This Documentation is related to the download.py

### Classes and Functions
This Python file has 0 classes and contains 4 functons

Functions:

Function 1: list_ext

Function 2: list_folder

Function 3: list_files

Function 4: download_file

### Requirements
    1)google.auth
    2)googleapiclient
    3)os
    4)shutil
    
### Import
    1)os
    2)shutil
    3)Request
    4)Credentials
    5)InstalledAppFlow
    6)HttpError
    7)MediaIoBaseDownload
    8)build
### How to Use
To get the list of folders with extensions present in each of them:
```
=>list_folder()
=>list_folder() calls list_ext(folder_id) which takes folder_id as an arguement
```


To get the list of files present in a folder with an id:
```
=>list_files(folder_id)
```

To download a file with an id:
```
=>download_file(file_id)
```
    
    
   
   
