from flask import Flask, escape, request, json, jsonify
import requests
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import os


# pip install flask_sqlalchemy
# pip install flask_script    
# pip install flask_migrate   
# pip install psycopg2-binary 

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'TestetyEst373573'

#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import model

#Set the Alpha Vantage API KEY
ALPHA_VANTAGE_KEY = 'PE3J13GZ7V9GOPKO'

@app.route('/')
def hello():
    return "Hello World"

#Show Ibovespa points
@app.route('/ibovespa/points')
def showIbovespaPoints():
    return jsonify(getCompanyPointsFromAPI("^BVSP"))

#Show Ibovespa points
@app.route('/points/<companyName>')
def showPointsForCompany(companyName):
    if not companyName:
        return jsonify({"status": 404, "message": "You need to inform a valid company code to access this resource"})
    return jsonify(getCompanyPointsFromAPI(companyName))



#---------------------------------------#


def getCompanyPointsFromAPI(companyName):
    messageReturn = {}
    #call to URL API
    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+companyName+"&apikey=" + ALPHA_VANTAGE_KEY + ""
    #Getting the values from API
    apiRequest = requests.get(url)
    #Check if has an error
    if(apiRequest.status_code != 200):
        messageReturn =  { "status" : apiRequest.status_code, "message": "Something went wrong" }
    else:
        #Parse data to python object
        response = json.loads(apiRequest.content)
        if 'Error Message' in response:
            messageReturn =  { "status" : 204, "message": "You need to inform a valid company code to access this resource" }
        #Check if has a result
        elif not 'Global Quote' in response:
            messageReturn =  { "status" : 503, "message": "Something went wrong" }
        #Getting the last value of Ibovespa
        else:
            currentPoints = response['Global Quote']['05. price']
            messageReturn = { "status" : apiRequest.status_code, "current_points": currentPoints }

    return messageReturn

    
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True) 