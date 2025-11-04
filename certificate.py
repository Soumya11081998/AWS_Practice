import boto3
import botocore
import certifi

session = boto3.session.Session()
s3 = session.client('s3', config=botocore.config.Config(ssl_ca_bundle=certifi.where()))