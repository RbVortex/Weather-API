from flask import Flask, render_template, request #Import template folder
import requests #sends requests to URLs

class WeatherAPI : #declares class called WeatherAPI
    def __init__(self) : #Class constructor function
        self.apiKey = 'c5cd3f6987ff37a7c216c93d22c2d9cc' #Generated API key
        self.geoKey = 'uk' #Sets location for API


    def ConvertKelvinToCelcius(self, kelvin) : #Declared function
        return round(kelvin - 273.15, 2) #Algorithm created to display degrees celcius

# object variable
wAPI = WeatherAPI()

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def indexDisplay(): #declare function
    return render_template('index.html') #Returns index from templates folder

@app.route('/temperature', methods=['POST']) # <form method="POST
def tempDisplay(): #declare function
    cityname = request.form['city']

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cityname+',' + wAPI.geoKey + '&APPID=' + wAPI.apiKey) #Submits the API query
    if r.ok == False : #If unacceptable characters entered, returns to index
        return render_template("index.html")
    json_object = r.json() #Stores json into json_object variable
    temp_k = float(json_object['main']['temp']) #Selects main & temp from json_object and converts to float
    temp_c = wAPI.ConvertKelvinToCelcius(temp_k) #Converts from kelvin to degrees celcius
    return render_template("temperature.html", temp=temp_c, city=cityname) #Renders temperature page from templates folder


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
