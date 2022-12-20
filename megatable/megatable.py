import psycopg2
import boto3
import os
from datetime import date
import zipfile

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
def upload():
    for i in range(2,11):
        if(os.path.exists(f'{i}annotations')):
            for file in os.listdir(f'{i}annotations'):
                if(file):

                    s3.Bucket('megatabletest').upload_file(
                        Filename=f'{i}annotations/'+file, Key='annotations/'+file)
    print("file uploaded")




# Insert data
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

        if (url.split("/",4)[3] == 'required_bucket'):

            img.append(url)


        if(url.split("/",4)[3]=='labels'):
            if (url =='https://megatabletest.s3.amazonaws.com/labels/'):
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

    id=428
    d=1
    for i in range(len(ann)):
        if ann_name[i] in img_name:
            index=img_name.index(ann_name[i])
            fid=f'f0{id}'
            # cursor.execute('''insert into frame (
            #            frame_id,frame_url) values
            #            (%s,%s)
            #
            #            ''', (fid,img[i]))

            aid=f'a0{d}'
            cursor.execute('''insert into training2 (
            artifact_id,
            frame_id,frame_date,
            customer_id,
            artifact_type,
            bounding_boxes_url,
            artifact_usage,
            video_url,
            frame_metadata_json) values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)

            ''',(aid,fid,date(2022,12,15),1002,1,ann[i],"True","",""))

            id += 1
            d+=1



def create():
    cursor.execute('''create table train2 (
    frame_id varchar(255) not null references frame(frame_id),
    frame_date date not null,
    customer_id int references customer_reference(customer_id),
    artifact_type int not null references artifact_reference(artifact_type),
    bounding_boxes_url varchar(255) ,
    video_url varchar(65535),
    frame_metadata_json varchar(65535))
    ''')



# Delete data
def delete(table_name):
    id = input("Enter frame_id you want to delete")
    cursor.execute('''DELETE FROM FRAME WHERE frame_id= %s ''', (id,))


def view(table_name):
    print(table_name)
    cursor.execute('''SELECT * FROM (%s) ''')
    # result = cursor.fetchall();
    # print(result)

def download():
    folder_name = "downloads"  # _where_all_files need to save

    DOWNLOAD_LOCATION_PATH = folder_name
    if not os.path.exists(DOWNLOAD_LOCATION_PATH):
        os.makedirs(DOWNLOAD_LOCATION_PATH)


    my_bucket = s3.Bucket('megatabletest')
    for my_bucket_object in my_bucket.objects.all():
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'megatabletest',

                'Key': my_bucket_object.key
            }
        )

        if('required_bucket' in my_bucket_object.key):
            s3_client.download_file('megatabletest',my_bucket_object.key,DOWNLOAD_LOCATION_PATH)
            zipfile_name = folder_name + '.zip'
            zipfile_path = zipfile_name

            zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)
            zipdir = DOWNLOAD_LOCATION_PATH

            for root, dirs, files in os.walk(zipdir):
                for file in files:
                    zipf.write(os.path.join(root, file))
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
download()




conn.commit()
conn.close()
