"""Web app."""
import flask
from flask import Flask, render_template, request, redirect, url_for

import pickle
import base64
from training import prediction
import requests



app = flask.Flask(__name__)

data = [{'name':'Delhi', "sel": "selected"}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}]
# data = [{'name':'India', "sel": ""}]
months = [{"name":"May", "sel": ""}, {"name":"June", "sel": ""}, {"name":"July", "sel": "selected"}]
cities = [{'name':'Delhi', "sel": "selected"}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}, {'name':'New York', "sel": ""}, {'name':'Los Angeles', "sel": ""}, {'name':'London', "sel": ""}, {'name':'Paris', "sel": ""}, {'name':'Sydney', "sel": ""}, {'name':'Beijing', "sel": ""}]

model = pickle.load(open("model.pickle", 'rb'))

@app.route("/")
@app.route('/login.html')
def login() -> str:
    """Base page."""
    return flask.render_template("login.html")
@app.route('/register.html')
def register():
    return render_template('register.html')
@app.route('/registrationform.php',methods=['GET','POST','DELETE'])
def registrationform():
    return "Account created successfully"

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/chennai.html')
def chennai():
    return render_template('chennai.html')

@app.route('/predicts.html')
def predicts():
    return render_template('predicts.html', cities=cities, cityname="Information about the city")

@app.route('/predicts.html', methods=["GET", "POST"])
def get_predicts():
    try:
        cityname = request.form["city"]
        cities = [{'name':'Delhi', "sel": ""}, {'name':'Mumbai', "sel": ""}, {'name':'Kolkata', "sel": ""}, {'name':'Bangalore', "sel": ""}, {'name':'Chennai', "sel": ""}, {'name':'New York', "sel": ""}, {'name':'Los Angeles', "sel": ""}, {'name':'London', "sel": ""}, {'name':'Paris', "sel": ""}, {'name':'Sydney', "sel": ""}, {'name':'Beijing', "sel": ""}]
        for item in cities:
            if item['name'] == cityname:
                item['sel'] = 'selected'
        print(cityname)
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        location = cityname
        api_key = 'Bwv2FJJQHT4FTQBWFC7IEKRE49lNYtrAti6NK7uJVCY' # Acquire from developer.here.com
        PARAMS = {'apikey':api_key,'q':location} 
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']
        final = prediction.get_data(latitude, longitude)

        final[4] *= 15
        if str(model.predict([final])[0]) == "0":
            pred = "Safe"
        else:
            pred = "Unsafe"
        
        return render_template('predicts.html', cityname="Information about " + cityname, cities=cities, temp=round(final[0], 2), maxt=round(final[1], 2), wspd=round(final[2], 2), cloudcover=round(final[3], 2), percip=round(final[4], 2), humidity=round(final[5], 2), pred = pred)
    except:
        return render_template('predicts.html', cities=cities, cityname="Oops, we weren't able to retrieve data for that city.")

if __name__ == "__main__":
    app.run(debug=True)
