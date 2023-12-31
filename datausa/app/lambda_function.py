import requests
import io
import json
import pandas as pd
# from bs4 import BeautifulSoup
import boto3
import csv
import re


def connect_to_endpoint(url):
    response = requests.request("GET", url)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def lambda_handler(event, context):
    bucketname = 'mthis-rearc'
    prefix = 'datausa_data/'
    api = 'https://datausa.io/api/data?drilldowns=Nation&measures=Population&year=latest'
    filename = 'us_pop_data'

    response = connect_to_endpoint(api)

    # Check year returned 
    # if response['data'][0]['Year'] ==       

    df = pd.DataFrame.from_dict(response['data'])
    df.to_csv('/tmp/'+filename+".csv", index=False)

    s3 = boto3.resource('s3')    
    s3.Bucket(bucketname).upload_file('/tmp/'+filename+".csv", prefix+filename+".csv")

    return {
            'statusCode': 200,
            'body': json.dumps('Lambda successfully completed!')
        }