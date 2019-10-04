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

app.config.from_object(os.environ['APP_SETTINGS'])
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

#
# Routes from User management
#
@app.route("/user/add", methods=['POST'])
def add_book():
    name=request.form.get('name')
    company=request.form.get('company')
    document=request.form.get('document')
    username=request.form.get('username')
    password=request.form.get('password')
    try:
        user=model.User(
            name=name,
            company=company,
            document=document,
            username=username,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return "User registered successfully with id={}".format(user.id)
    except Exception as e:
	    return(str(e))


@app.route("/users/all")
def get_all():
    try:
        users=model.User.query.all()
        return  jsonify([e.serializeWithoutPassword() for e in users])
    except Exception as e:
	    return(str(e))

@app.route("/user/get/<id_>")
def get_by_id(id_):
    try:
        user=model.User.query.filter_by(id=id_).first()
        return jsonify(user.serializeWithoutPassword())
    except Exception as e:
	    return(str(e))

@app.route("/user/update" , methods=['PUT'])
def updateUser():
    id_ = request.form.get('id')
    name=request.form.get('name')
    company=request.form.get('company')
    document=request.form.get('document')
    password=request.form.get('password')
    try:
        user=model.User.query.filter_by(id=id_).first()
        user.name = name
        user.company = company
        user.document = document
        user.password = password
        db.session.commit()
        return "User updated successfully !"
    except Exception as e:
	    return(str(e))
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