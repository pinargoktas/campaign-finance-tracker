import logger
from zipfile38 import ZipFile
from zipfile38 import is_zipfile
import zipfile38
from google.cloud import storage
import wget
import pandas as pd
import os

from flask import Flask
from secure import require_apikey


app = Flask(__name__)

@app.route('/health')
def health():
    return 'It is alive!\n'

@app.route('/data_puller')
def data_puller():
    url = os.environ.get['URL']
    bucket_name = os.environ.get['BUCKET'] #without gs://
    file_name = os.environ.get['FILE_NAME']
    client = storage.Client($PROJECT_ID)
    cf_path = '/tmp/{}'.format(file_name)

    bucket = client.get_bucket(bucket_name)
    wget.download(url, cf_path)
    blob = storage.Blob(file_name, bucket)
    blob.upload_from_filename(cf_path)

    print("""This Function was triggered by messageId published at""")
    
@app.route('/unzipper')
def unzipper():
    storage_client = storage.Client($PROJECT_ID)
    bucket = storage_client.get_bucket(os.environ.get['BUCKET'])

    destination_blob_pathname = os.environ.get['FILE_NAME']
        
    blob = bucket.blob(destination_blob_pathname)
    zipbytes = io.BytesIO(blob.download_as_string())
    
    if is_zipfile(zipbytes):
        with ZipFile(zipbytes, 'r') as myzip:
            for contentfilename in myzip.namelist():
                contentfile = myzip.read(contentfilename)
                blob = bucket.blob(zipfilename_with_path + "/" + contentfilename)
                blob.upload_from_string(contentfile)
             
