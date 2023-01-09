from dotenv import load_dotenv
import psycopg2
import boto3
import os



load_dotenv('config.env')

database_url=f"postgresql+psycopg2://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@localhost:5433/{os.environ.get('DATABASE')}"


conn = psycopg2.connect(
    database=os.environ.get("DATABASE"),
    user=os.environ.get('USERNAME'),
    password=os.environ.get('PASSWORD'),
    host="localhost",
    port="5433"
)


s3 = boto3.resource(
    service_name='s3',
    region_name=os.environ.get('REGION'),
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('SECRET_KEY')
)

s3_client = boto3.client(
    service_name='s3',
    region_name=os.environ.get('REGION'),
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('SECRET_KEY')
)
