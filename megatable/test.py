import unittest
from init import conn,s3
import random
import megatable

obj = megatable.Megatable()

cursor = conn.cursor()

my_bucket = s3.Bucket('megatabletest')

class MyTestCase(unittest.TestCase):

    def test_download(self):
        q = 'select f.frame_url from training as t inner join frame as f on t.frame_id=f.frame_id where f.frame_id=\'f0100\';'
        print(q)
        res = obj.download(q)
        assert res == 'downloads.zip', res

    def test_upload(self):
        test_count = 0
        count = obj.upload("test")
        for bucket in my_bucket.objects.all():

            if 'test/' in bucket.key:
                test_count += 1
        assert test_count == count


if __name__ == '__main__':
    unittest.main()
 
