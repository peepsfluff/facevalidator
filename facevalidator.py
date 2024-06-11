# aws lambda function python 3.9 

import json
import sys 
import os 
import boto3
import base64



def write_to_file(save_path,data):
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(data))
        

def lambda_handler(event, context):
# boto3 sdk for python to call rekognition aws service 

    client = boto3.client('rekognition')
    
    #{ "photo": "/jpegsdkjflskdflskjdf"}
    encodeImage= event['photo']
    encodeImage = encodeImage [23:] 
   
    write_to_file('/tmp/face.jpg',encodeImage)
    #/tmp/face.jpg is referring to /tmp folder that is available to a lambda function only at runtime 
    #cannot physically open up /tmp  only available to lambda function while it runs 
    
    
    try:
        imgFile = open('/tmp/face.jpg', 'rb')
        #open up the file that is saved to /tmp folder 
        imgBytes = imgFile.read()
        #read the bytes in
        imgFile.close()
    except: 
        print('Could not read the file')
    
    imgobj = {'Bytes': imgBytes} 
    #create json object with the bytes as the imgBytes variable 

    # rekognition api is expecting: 
    # Image = { "Bytes": "sldkfjsdfbytes" }
    
    #response_labels = client.detect_labels(Image=imgobj)
    response_labels = client.detect_faces(Image=imgobj) 
    
    print(response_labels)
    return {
        # 'statusCode': 200,
        'body': json.dumps(response_labels)
    }




