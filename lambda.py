import json
import urllib.parse
import boto3
import random

print('Loading function')

dynamo = 'gregs-image-table'
s3 = boto3.client('s3')
rekog = boto3.client('rekognition')
dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    
    print("")
    print("lambda handler")
    print("getting image from s3....")
    s3o = event["Records"][0]["s3"]
    bucket = s3o['bucket']['name']

    print("object key:")
    key = s3o["object"]["key"]
    print(key)
    # key = urllib.parse.unquote_plus(key, encoding='utf-8')
    print("")

    print("object size:")
    size = s3o["object"]["size"]
    print(size)
    print("")

    print("")

    # Get the image from s3 bucket 
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {} '.format(key, bucket))
        raise e
    else:
        print ()
        
    # Get labels from rekognition
    ls = labels(key, bucket)
        
    # Create a new table with labels from rekognition
    # create_table(key, ls)    
        
    # Add to dynamo table
    dynamo_add(key, ls)
        
        
def labels(photo, bucket):
    
    print("")
    print("Getting labels from rekognition")
    print("Bucket: %s" % (bucket))
    print("Photo: %s" % (photo))
    print("")
    
    response = rekog.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)


    print('Detected labels for ' + photo) 
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
   
    return response['Labels']


def dynamo_add(img_id, labels):
    
    (img, ext) = img_id.split('.')
    print("")
    print("")
    print("Adding labels to dynamo table....")
    print("File: %s" % (img))
    print("Type: %s" % (ext))
    
    # Define loops as 5, if there are fewer labels returned from rekog then rewrite loops
    loops = 5
    if len(labels) < loops:
        loops = len(labels)

    # traverse the labels and extract Name value
    labels_list = []    
    for l in labels:
        labels_list.append(l["Name"])
    print("Labels found for %s: %s" %(img_id, labels_list))
    
    
	
    print("")
    labels_dict = [{"S": f} for f in labels_list[:loops]]
    print("Adding to gregs-image-table-> Key:%s  Labels:%s" %(img_id, labels_dict))
    print("")
    print("")
    print("")
    
    dynamo.put_item(
            TableName='gregs-image-table',
            Item={
                'img_name': {
                    'S': img
                    
                },
                'Labels': {
                    'L': labels_dict
                }
            }
    )