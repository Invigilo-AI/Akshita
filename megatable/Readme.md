## This Documenatation is for the Megatable POC version 0
#### Functions used are
1) Create : Creates schema for a table
2) Insert : Lets you insert data into the table
3) Delete : Data from the table can be deleted
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
    
