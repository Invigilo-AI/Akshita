## This Documenatation is for the Megatable POC version 0
## Megatable.py
#### Functions built are
1) Insert : Lets you insert data into the table
2) Delete : Data from the table can be deleted
3) Show_Table : Displays the result based on query
4) Upload : Folders can be uploaded to the S3 bucket
5) Download : Based on the query entered corresponding images/annotations are downloaded in thw form of a zip file from the S3 bucket<br><br>
Sample queries:<br><br>
  <i>fetch frame_urls from frame table</i><br>
    ```
    Select frame_url from frame;
    ```
  
   <i>fetch annotations from training table</i><br>
   ```
   Select bounding_boxes_url from training;
   ```
   <i>fetch frame_urls that are of artifact_type=2 (Hook)</i><br>
   ```
   Select f.frame_url from 
   training as t inner join frame as f 
   on t.frame_id=f.frame_id 
   where t.artifact_type=1;
   ```
    How to Run
    <ul>
    <li> An environment file is to be made with postgres db and AWS credentials:<br>
    1) REGION<br>
    2) ACCESS KEY<br>
    3) SECRET KEY<br>
    4) DATABASE<br>
    5) USER<br>
    6) PASSWORD<br>
    </li>
    <li> Once created save it is as .env file in the same directory.
    </li>
    <li>Then run the following command:</li><br>
    </ul>
    
    ```
    python3 megatable.py
    ```
    
For more documentation :
https://docs.google.com/document/d/16IsBlLL3e48tWh0jDiZgcq_qLBwOPqAL9LFm0bJ5rL4/edit?usp=sharing

## Testing
#### Test.py contains test functions which are as follows:
1) test_one_upload : It uploads folder to the S3 bucket and checks the no. of files uploaded is same as the no. of files in the folder.
2) test_two_insert : It inserts frame_id and frame_url into the test table.Frame_url is same as that of the uploaded file url in the S3 bucket.
3) test_three_download : It downloads files in the form of zip based on the entered query.It checks if the zip file downloaded is empty or not.

How to Test

1)Create a Test_folder in the same directory containing jpg/txt files.

2)Install pytest

3)Run ./test.sh

```
pip install pytest
./test.sh
```



