import os
# currentdir = os.path.dirname(os.path.realpath(__file__))
# print(currentdir)
# parentdir = os.path.dirname(currentdir)
# parentdir2 = os.path.dirname(parentdir)
# print(parentdir2)
# sys.path.append(parentdir2)


from test_model import Base, Frame_test
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from init import s3, database_url, conn, s3_client
from megatable import Megatable

obj = Megatable()

cursor = conn.cursor()

my_bucket = s3.Bucket('megatabletest')

engine = create_engine(database_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()


def get_url(folder):
    for bucket in my_bucket.objects.all():

        if folder in bucket.key:
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'megatabletest',
                    'Key': bucket.key
                }
            )
            url = url.split("?")[0]

            return url

# Test Functions

# Test function to upload files to S3 bucket
def test_one_upload():
    test_count = 0
    count = obj.upload("test_folder")
    for bucket in my_bucket.objects.all():
        if 'test_folder/' in bucket.key:
            test_count += 1

    assert test_count == count

# Test function to insert into test table
def test_two_insert():
    url = get_url('test_folder/')

    frame1 = Frame_test(
        frame_id='f01',
        frame_url=url )
    
    s.add(frame1)
    s.commit()

    assert frame1.frame_id == 'f01'
    assert frame1.frame_url == url

# Test function to download files based on query
def test_three_download():
    q = 'select frame_url from frame_test where frame_id = \'f01\';'
    res = obj.download(q)
    assert os.stat("downloads.zip").st_size > 0, res
