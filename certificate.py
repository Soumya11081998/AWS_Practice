import boto3
import botocore
import certifi

session = boto3.session.Session()
s3 = session.client('s3', config=botocore.config.Config(ssl_ca_bundle=certifi.where()))

# ~/.aws/credentials
[default]
aws_access_key_id = 341124395777
aws_secret_access_key = AKIAU63EZGMAZAYGEP6G