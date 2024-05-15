from flask import Flask

app = Flask(__name__)

from app import routes


import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv('DEBUG')

app.run(debug=False)
