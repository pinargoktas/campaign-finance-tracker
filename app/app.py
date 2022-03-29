import logger
import os
from zipfile38 import ZipFile
from zipfile38 import is_zipfile
import zipfile38
from google.cloud import storage
import wget
import pandas as pd

from flask import Flask
from secure import require_apikey


app = Flask(__name__)

@app.route('/health')
def health():
    return 'It is alive!\n'

@app.route('/data_puller')
def data_puller():
    url = os.environ[${_URL}]
    bucket_name = os.environ[${_BUCKET}] #without gs://
    file_name = os.environ[${_FILE_NAME}]
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
    bucket = storage_client.get_bucket(${_BUCKET})

    destination_blob_pathname = ${_FILE_NAME}
        
    blob = bucket.blob(destination_blob_pathname)
    zipbytes = io.BytesIO(blob.download_as_string())
    
    if is_zipfile(zipbytes):
        with ZipFile(zipbytes, 'r') as myzip:
            for contentfilename in myzip.namelist():
                contentfile = myzip.read(contentfilename)
                blob = bucket.blob(zipfilename_with_path + "/" + contentfilename)
                blob.upload_from_string(contentfile)
             
@app.route('/txt2csv')
def txt2csv():
    fileName = ${_FILE_NAME}
    if ${_FILE_NAME}[:-3] == '.txt'
        df = pd.read_csv(fileName, sep=",")

        storage_client = storage.Client($PROJECT_ID)
        bucket = client.get_bucket(${_BUCKET})
        blob = bucket.blob(${_FILE_NAME})
 	    blob.upload_from_string(df.to_csv(), 'text/csv')

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
