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
def addUser():
    name=request.form.get('name')
    company=request.form.get('company')
    document=request.form.get('document')
    username=request.form.get('username')
    password=request.form.get('password')
    if not checkIfCompanyExistsById(company):
        return "Company id is not valid !"
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
	    return("Ops, something went wrong, please try again later !")


@app.route("/users/all")
def getAllUsers():
    try:
        users=model.User.query.all()
        return  jsonify([e.serializeWithoutPassword() for e in users])
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/user/get/<id_>")
def getUserById(id_):
    try:
        user=model.User.query.filter_by(id=id_).first()
        return jsonify(user.serializeWithoutPassword())
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/user/update" , methods=['PUT'])
def updateUser():
    id_ = request.form.get('id')
    name=request.form.get('name')
    company=request.form.get('company')
    document=request.form.get('document')
    password=request.form.get('password')
    if not checkIfCompanyExistsById(company):
        return "Company id is not valid !"
    try:
        user=model.User.query.filter_by(id=id_).first()
        user.name = name
        user.company = company
        user.document = document
        user.password = password
        db.session.commit()
        return "User updated successfully !"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/user/delete", methods=['DELETE'])
def deleteUser():
    id_ = request.form.get('id')
    try:
        user=model.User.query.filter_by(id=id_).first()
        db.session.delete(user)
        db.session.commit()
        return "User removed successfully"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")



#
# Routes from Company management
#
@app.route("/company/add", methods=['POST'])
def addCompany():
    name=request.form.get('name')
    financial_code=request.form.get('financialCode')
    if checkIfCompanyExistsByFinancialCode(financial_code):
        return "This financial code already exists in our database !"
    try:
        company=model.Company(
            name=name,
            financial_code=financial_code
        )
        db.session.add(company)
        db.session.commit()
        return "Company registered successfully with id={}".format(company.id)
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")


@app.route("/companies/all")
def getAllCompanies():
    try:
        companies=model.Company.query.all()
        return  jsonify([e.serialize() for e in companies])
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/get/<id_>")
def getCompanyById(id_):
    try:
        company=model.Company.query.filter_by(id=id_).first()
        if company is None:
            return "No company finds"
        return jsonify(company.serialize())
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/update" , methods=['PUT'])
def updateCompany():
    id_ = request.form.get('id')
    name=request.form.get('name')
    financial_code=request.form.get('financialCode')
    try:
        company=model.Company.query.filter_by(id=id_).first()
        company.name = name
        if company.financial_code != financial_code and checkIfCompanyExistsByFinancialCode(financial_code):
            return "This financial code already exists on our database"
        company.financial_code = financial_code
        db.session.commit()
        return "Company updated successfully !"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/delete", methods=['DELETE'])
def deleteCopmpany():
    id_ = request.form.get('id')
    try:
        company=model.Company.query.filter_by(id=id_).first()
        db.session.delete(company)
        db.session.commit()
        return "Company removed successfully"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")


#
# Routes from Company Points management
#
@app.route("/company/value/set", methods=['POST'])
#Add or update the company points
def setCompanyValue():
    id_company_=request.form.get('id_company')
    try:
        company=model.Company.query.filter_by(id=id_company_).first()
        #Check if company exists on  database
        if company is None:
            return "No company finds"
        #getting the points from API
        companyPoints = getCompanyPointsFromAPI(str(company.financial_code))
        #Verify if return points
        if not 'current_points' in companyPoints:
            return "We can't find the points from this company"

        #Getting company value from DB
        companyValueDB = model.CompanyValue.query.filter_by(id_company=id_company_)
        if companyValueDB.first() is None: #Add company value to database
            companyValue=model.CompanyValue(
                id_company=id_company_,
                market_points=companyPoints['current_points']
            )
            db.session.add(companyValue)
            db.session.commit()
            return "Company points registered successfully, current points to this company: {}".format(companyValue.market_points)
        else: #Update company value on database
            companyValueDB = companyValueDB.first()
            companyValueDB.market_points = companyPoints['current_points']
            db.session.commit()
            return "Company points updated successfully !"
    except Exception as e:
	    return str(e)
        #return("Ops, something went wrong, please try again later !")


@app.route("/companies/values/all")
def getAllCompaniesValues():
    try:
        companiesValues=model.CompanyValue.query.all()
        return  jsonify([e.serialize() for e in companiesValues])
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/value/get/<id_>")
def getCompanyValueById(id_):
    try:
        company=model.Company.query.filter_by(id=id_).first()
        return jsonify(company.serialize())
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/value/update" , methods=['PUT'])
def updateCompanyValue():
    id_ = request.form.get('id')
    market_points=request.form.get('marketPoints')
    try:
        companyValue=model.CompanyValue.query.filter_by(id=id_).first()
        companyValue.market_points = market_points
        db.session.commit()
        return "Company points updated successfully !"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")

@app.route("/company/value/delete", methods=['DELETE'])
def deleteCompanyValue():
    id_ = request.form.get('id')
    try:
        companyValue=model.CompanyValue.query.filter_by(id=id_).first()
        db.session.delete(companyValue)
        db.session.commit()
        return "Company value removed successfully"
    except Exception as e:
	    return("Ops, something went wrong, please try again later !")
#
#--------------------------------------------------------------------------------------------#
#

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

def checkIfCompanyExistsById(idCompany):
    try:
        company=model.Company.query.filter_by(id=idCompany).first()
        if company is None:
            return False
        return True
    except Exception as e:
	    return False

def checkIfCompanyExistsByFinancialCode(financialCode):
    try:
        company=model.Company.query.filter_by(financial_code=financialCode).first()
        if company is None:
            return False
        return True
    except Exception as e:
	    return False
    
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True) 