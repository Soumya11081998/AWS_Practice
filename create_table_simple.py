import boto3

s3 = boto3.client('s3')
bucket_name = 'aws-s3-demo-bucket-soumya1998'
file_name = 'sample_upload.txt'
object_name = 'F:\AWS_Practice\sample_upload.txt'  # Optional path in bucket

# Upload file
s3.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ExpectedBucketOwner': 'af61611b443bac85f2d7a35a904298764defe0647833bdf61205af195c7b7530'})
print("File uploaded!")