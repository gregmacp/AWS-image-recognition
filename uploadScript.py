import boto3, random, os, botocore
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = '---'
SECRET_KEY = '---'
bucket_name = 'image-greg-macpherson'
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3res = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def download_image(file_s3, file_local):
    print("HERE: %s and %s" % (file_s3, file_local))
    try:
        s3res.Bucket(bucket_name).download_file(file_s3, file_local)
        print("Downloaded as %s" % file_local_download)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def upload_image(local_file, bucket, s3_file):

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        print("Uploaded as %s" % file_s3_upload)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# get user input
choice = input("What would you like to do? (upload / download) >")
target = input("Enter the name of the file eg.'landscape2.jpg' >")
if choice == "upload":
    print("executing upload...")
    # specify local path for file upload
    file_local_upload = "img/" + target
    # get extension for targeted upload file
    f, ext = os.path.splitext(file_local_upload)
    # specify s3 name
    file_s3_upload = 'img%s%s' % ((random.randint(100, 999)), ext)
    # call upload function
    uploaded = upload_image(file_local_upload, bucket_name, file_s3_upload)
if choice == "download":
    print("executing download...")
    # specify s3 path for file download
    file_s3_download = target
    # get extension for targeted download file
    f, d_ext = os.path.splitext(file_s3_download)
    # specify local download location
    file_local_download = 'img/img%s%s' % (random.randint(100, 999), d_ext)
    # call download function
    download_image(file_s3_download, file_local_download)



