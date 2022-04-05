import logger
#from zipfile38 import ZipFile
#from zipfile38 import is_zipfile
#import zipfile38
from google.cloud import storage
#import wget
#import pandas as pd
import os

from flask import Flask
from secure import require_apikey


application = Flask(__name__)


@application.route('/health')
def health():
    return 'It is alive!\n'

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=int(os.environ.get($PORT)))

