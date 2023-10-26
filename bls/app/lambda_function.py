import requests
import io
import json
import pandas as pd
from bs4 import BeautifulSoup
import boto3
import csv
import re



def lambda_handler(event, context):
    url = 'https://download.bls.gov/pub/time.series/pr/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
    bucketname = 'mthis-rearc'
    prefix = 'bls_data/'

    response = requests.get(url, headers=headers) 
    html = response.text  
    soup = BeautifulSoup(html, "lxml")
    regex = re.compile('.*/pub/time.series/.*')
    elements = soup.findAll('a' , {"href": regex})
    files = [i.text.strip() for i in elements if 'data.0' in i.text]
    for f in files:
        response = requests.get(url+f, headers=headers)
        filename = f.replace(".", "_")
        output = open(filename+'.csv', 'wb')
        output.write(response.content)
        output.close()

        s3 = boto3.resource('s3')    
        s3.Bucket(bucketname).upload_file(filename, prefix+filename)

    return {
            'statusCode': 200,
            'body': json.dumps('Lambda successfully completed!')
            # 'response': response['Items']  
        }