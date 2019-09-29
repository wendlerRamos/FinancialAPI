from flask import Flask, escape, request, json, jsonify
import requests
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TestetyEst373573'

#Set the Alpha Vantage API KEY
ALPHA_VANTAGE_KEY = 'PE3J13GZ7V9GOPKO'

@app.route('/')
def hello():
    #print(ALPHA_VANTAGE_KEY)
    return "Hello World"

#Show Ibovespa points
@app.route('/ibovespa/points')
def showIbovespaPoints():
    return jsonify(getIbovespaPointsFromAPI())

def getIbovespaPointsFromAPI():
    #call to URL API
    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^BVSP&apikey=" + ALPHA_VANTAGE_KEY + ""
    #Getting the values from API
    apiRequest = requests.get(url)
    #Check if has an error
    if(apiRequest.status_code != 200):
        return { "status" : apiRequest.status_code, "current_points": 0 }
    #Parse data to python object
    response = json.loads(apiRequest.content)
    #Getting the last value of Ibovespa
    currentPoints = response['Global Quote']['05. price']
    return { "status" : apiRequest.status_code, "current_points": currentPoints }

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)