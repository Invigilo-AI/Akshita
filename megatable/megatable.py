
from datetime import date
import zipfile
import requests
import shutil
import os
from init import s3,s3_client,database_url,conn
from sqlalchemy.orm import sessionmaker,session
from  models import *
from sqlalchemy import create_engine


cursor = conn.cursor()

engine = create_engine(database_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()

my_bucket = s3.Bucket('megatabletest')

class Megatable:


    # Upload data
    '''
    :input: folder - folder name that is to be uploaded on S3
    :output: Uploads the folder in the S3 bucket
    '''

    def upload(self,folder):

        # replace annotations by suitable folder name
        # for i in range(2, 11):
        if (os.path.exists(f'{folder}')):
            for file in os.listdir('1annotations'):
                if (file):
                    s3.Bucket('megatabletest').upload_file(
                        Filename=f'{folder}/' + file, Key=f'{folder}/' + file)
                    print("file uploaded")



    # Insert data into db
    def insert(self):

        ann = []
        img = []
        for my_bucket_object in my_bucket.objects.all():
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'megatabletest',

                    'Key': my_bucket_object.key
                }
            )
            url = url.split("?")[0]

            if (url.split("/", 4)[3] == 'images'):
                img.append(url)

            if (url.split("/", 4)[3] == 'labels'):
                if (url == 'https://megatabletest.s3.amazonaws.com/annotations/'):
                    continue

                f_url = url
                ann.append((f_url))

        img_name = []
        ann_name = []
        for i in range(len(img)):
            name = img[i].split("/", 4)[4].split(".")[0]
            img_name.append(name)

        for i in range(len(ann)):
            name = ann[i].split("/", 4)[4].split(".")[0]
            ann_name.append(name)

        id = 2445
        for i in range(len(ann)):
            if ann_name[i] in img_name:
                fid = f'f0{id}'

                # frame=Frame(
                #   frame_id=fid,
                #   frame_url=img[i]
                # )
                # s.add(frame)



                training=Training(
                    frame_id=fid,
                    frame_date=date(2022,12,15),
                    customer_id=1002,
                    artifact_type=2,
                    bounding_boxes_url=ann[i],
                    video_url="",
                    frame_metadata_json=""
                )
                s.add(training)

                id += 1

        s.commit()


    #Delete data into db
    def delete(self,table_name):

        d = session.query(Training).filter(Training.frame_id == 'f033')
        session.delete(d)
        session.commit()



    # for downloading images/annotations
    '''
    :input:query 
           Examples:
           1.Select frame_url from frame;
           -fetch frame_urls from frame table
    
           2.Select bounding_boxes_url from training;
           -fetch annotations from training table
    
           3.Select f.frame_url from 
           training as t inner join frame as f 
           on t.frame_id=f.frame_id 
           where t.artifact_type=1;
           -fetch frame_urls that are of artifact_type=1 (Hook)
           
    :output: downloads the frames or annotations in a zip file
    '''
    def download(self,query):
        ans = []
        try:
            cursor.execute(f'''{query}''')
            result = cursor.fetchall()
            print(result)


            for i in range(len(result)):
                ans.append(result[i][0])
            if len(ans)>0 :
                folder_name = "downloads"
                zipfile_name = folder_name + '.zip'
                zipfile_path = zipfile_name
                zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                i = 0
                while (i < len(ans)):

                    url = ans[i].split("?")[0]

                    file_name = url.split("/", 4)[4]
                    try:
                        r = requests.get(ans[i], stream=True)
                        with open(os.path.join(folder_name, file_name), 'wb') as fd:
                            for chunk in r.iter_content(chunk_size=128):
                                fd.write(chunk)
                        zipf.write(os.path.join(folder_name, file_name))
                    except:
                        print("something went wrong")
                    fd.close()
                    i += 1

                shutil.rmtree("downloads")
                zipf.close()
                return zipfile_name
            else:
                return "No file exists,check the query"

        except Exception as e:

               return e




obj=Megatable()
obj.delete('Training')


# query = input()
# obj.download(query)

