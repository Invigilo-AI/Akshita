import psycopg2
import boto3
import os
from datetime import date
import zipfile
import requests
import shutil

conn = psycopg2.connect(
    database="testdb", user='postgres', password='123', host='localhost', port='5433'
)

cursor = conn.cursor()

cursor.execute("select version()")
data = cursor.fetchone()
print("Connection established to: ", data)

s3 = boto3.resource(
    service_name='s3',
    region_name=os.getenv('REGION'),
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY')
)

s3_client = boto3.client(
    service_name='s3',
    region_name=os.getenv('REGION'),
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY')
)

# Upload data
'''
:input: folder - folder name that is to be uploaded on S3
:output: Uploads the folder in the S3 bucket
'''
def upload(folder):
    #replace annotations by suitable folder name
    for i in range(2,11):
        if(os.path.exists(f'{i}annotations')):
            for file in os.listdir(f'{i}annotations'):
                if(file):

                    s3.Bucket('megatabletest').upload_file(
                        Filename=f'{i}annotations/'+file, Key='annotations/'+file)
    print("file uploaded")


# Insert data into db
def insert():
    my_bucket = s3.Bucket('megatabletest')

    ann=[]
    img=[]
    for my_bucket_object in my_bucket.objects.all():
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'megatabletest',

                'Key': my_bucket_object.key
            }
        )
        # insert(url,id)


        url = url.split("?")[0]

        if (url.split("/",4)[3] == 'images'):

            img.append(url)


        if(url.split("/",4)[3]=='annotations'):
            if (url =='https://megatabletest.s3.amazonaws.com/annotations/'):
                continue

            f_url=url

            ann.append((f_url))

    img_name=[]
    ann_name=[]
    for i in range(len(img)):
        name=img[i].split("/",4)[4].split(".")[0]

        img_name.append(name)


    for i in range(len(ann)):
        name = ann[i].split("/", 4)[4].split(".")[0]
        ann_name.append(name)

    id=2445
    d=1
    for i in range(len(ann)):
        if ann_name[i] in img_name:

            fid=f'f0{id}'
            # cursor.execute('''
            # insert into frame
            # (frame_id,frame_url) values
            # (%s,%s) ''',(fid,img[i]))

            cursor.execute('''insert into training (
            frame_id,frame_date,
            customer_id,
            artifact_type,
            bounding_boxes_url,
            artifact_usage,
            video_url,
            frame_metadata_json) values
            (%s,%s,%s,%s,%s,%s,%s,%s)

            ''',(fid,date(2022,12,15),1002,2,ann[i],"True","",""))



            id += 1
            d+=1


# create schema
def create():
    cursor.execute('''create table training (
    frame_id varchar(255) not null references frame(frame_id),
    frame_date date not null,
    customer_id int references customer_reference(customer_id),
    artifact_type int not null references artifact_reference(artifact_type),
    bounding_boxes_url varchar(255) ,
    artifact_usage boolean,
    video_url varchar(65535),
    frame_metadata_json varchar(65535))
    ''')


# Delete data into db
def delete(table_name):
    id = input("Enter frame_id you want to delete")
    cursor.execute('''DELETE FROM FRAME WHERE frame_id= %s ''', (id,))



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
       -fetch frame_urls that are of artifact_type=2 (Hook)

:output: downloads the frames or annotations in a zip file

'''
def download(query):
    ans=[]
    cursor.execute(f'''{query}''')
    result = cursor.fetchall();
    print(result)
    for i in range(len(result)):
        ans.append(result[i][0])
    folder_name = "downloads"
    zipfile_name = folder_name + '.zip'
    zipfile_path = zipfile_name
    zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)


    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    i=0
    while(i<len(ans)):

            url = ans[i].split("?")[0]

            file_name=url.split("/",4)[4]
            try:
                r = requests.get(ans[i], stream=True)
                with open(os.path.join(folder_name,file_name), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                zipf.write(os.path.join(folder_name,file_name))
            except:
                print("something went wrong")
            fd.close()
            i+=1



    shutil.rmtree("downloads")
    zipf.close()




# cursor.execute('''SELECT *
# FROM pg_catalog.pg_tables
# WHERE schemaname != 'pg_catalog' AND
#     schemaname != 'information_schema'; ''')
# result = cursor.fetchall();
# print("Select the table")
# for i in range(len(result)):
#     print(f"{i + 1}", result[i][1])
# n = int(input())
# table_name = result[n - 1][1]
#
# print("Choose an operation ")
# print("1.Insert\n2.Delete\n3.View")
# op = int(input())
# if (op == 1):
#     insert()
# elif (op == 2):
#
#     delete(table_name)
# else:
 # view(table_name)


# create()
#insert()

query=input()
download(query)

conn.commit()
conn.close()
