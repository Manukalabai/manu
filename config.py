from flask import Flask
import os
from flask_mpesa import MpesaAPI
from dotenv import *


app=Flask(__name__,template_folder="templates",static_folder="public")
app.secret_key='Manukalabai'

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/public/carimages"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER




mpesa_api=MpesaAPI()
load_dotenv()
app.config['API_ENVIRONMENT'] = os.getenv("API_ENVIRONMENT")
app.config['APP_KEY'] = os.getenv("APP_KEY")
app.config['APP_SECRET']=os.getenv("APP_SECRET")
mpesa_api.init_app(app)
