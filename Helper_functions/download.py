from __future__ import print_function
import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

import shutil



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


def list_ext(folder_id):

    """
    Lists all the extensions present in a given folder
    :input: Parameters for the function with the following keys:
        - folder_id: id of the folder
        
    :return: list of extensions present in the folder

    """

    try:
        service = build('drive', 'v3', credentials=creds)
        files=[]
        page_token = None
        
        while True:
            response = service.files().list(q = "'" + folder_id + "' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            
            for file in response.get('files', []):
                # Process change
                if( '.' in file.get('name')):
                    file_ext=file.get("name").rsplit(".",1)[1]
                    # print(f"file extension found: '{file_ext}'")
                    files.append(file_ext)
                
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
            print(F'An error occurred: {error}')
            files = None

    return files

def list_folder():
    """
    Lists all the folders present in the drive

    """
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        folders=[]
        page_token = None
        while True:
            response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            for folder in response.get('files', []):
                # Process change
                print(F'Found folder: {folder.get("name")}, {folder.get("id")}')
                folder_id=folder.get("id")
            
                file_ext=list_ext(folder_id)
                if(len(file_ext) >0):
                    print("Extensions")
                    print(set(file_ext))
                else:
                    print("No extensions")
                
            folders.extend(response.get('files', []))
            
                
            
            
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        folders = None
    
    
    return folders




def list_files(id,type):

    """
    Lists all the files present in the selected folder

    :input: Parameters for the function with the following keys:
        - id: id of the selected folder
        - type: type of file(zip/jpeg/png) to be downloaded
    
    :return: list of files

    """

    if(type=='zip'):
        type='application/zip'
    elif(type=='jpeg' or type=='jpg'):
        type='image/jpeg'
    elif(type=='png'):
        type='image/png'
    elif(type=='pdf'):
        type='application/pdf'
    
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files=[]
        page_token = None
        while True:
            
            response = service.files().list(q= f"mimeType=\'{type}\'and'" + id + "' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
                                      
            for file in response.get('files', []):
                # Process change
                
                print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
    if(files):
        
        return files
    else:
        print(f"No files available")
        
            
def download_file(file_name,id,type):
        """
        Download the file

        :input: Parameters for the function with the following keys:
             - file_name: file to be downloaded
             - id: id of the file to be downloaded
             - type: type of the file to be downloaded
    
        :return: file is downloaded in the same directory

        """
     
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_id = id
            request = service.files().get_media(fileId=file_id)
                                                
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')
                file.seek(0)
              
                # Write the received data to the filepics
                with open(f'{file_name}.{type}', 'wb') as f:
                    shutil.copyfileobj(file, f)

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.getvalue()


print("Listing all folders\n")
files=list_folder()

print("\n")
print("Enter the id of the selected folder\n")
folder_id=input()
print("Enter the type of file to be downloaded")
type=input()
files=list_files(folder_id,type)

if(files):
    print("Enter filename to be downloaded")
    file_name=input()
    print("Enter the id of the file")
    file_id=input()

    download_file(file_name,file_id,type)  


