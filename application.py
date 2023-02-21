# Clone the repo and run pip install requirements.txt
# python version 3.7

from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from challenge_azure.Pdfcreater import Pdfcreater
from challenge_azure.Check import Database
from challenge_azure import Dbconnection
import os
import logging
logging.basicConfig(filename='log/app.log', filemode='w',level=logging.INFO)

application = Flask(__name__) # initializing a flask app
app=application

@app.route('/')
@cross_origin()
def home():
    if request.method == 'GET':
        connection = Dbconnection.DB()
        mongo_db= connection.mongo()
        c_details = mongo_db['course_details']
        course = c_details.find().limit(25)
        path = os.path
        return render_template("home.html",result = course, path=path)

@app.route('/grabe-all')
@cross_origin()
def graball():
    grabcat = Pdfcreater()
    grabcat.grab_category()
    return "Nothig"

@app.route('/create-table')
@cross_origin()
def create_database():
    create = Database()
    create.create_table()
    create.mongo_test()
    return "Database updated Done!"





if __name__ == '__main__':
    app.run()

