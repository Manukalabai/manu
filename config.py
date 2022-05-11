from flask import Flask
import os


app=Flask(__name__,template_folder="templates",static_folder="public")
app.secret_key='Manukalabai'

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/public/carimages"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER