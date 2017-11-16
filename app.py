#!env\Scripts python.exe

from flask import Flask, render_template, request, url_for, redirect, session
import pygal
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required, Length
import requests
import math

# from pygal.style import LightSolarizedStyle
# This program is designed to use the Open Weather App API
# And recived a zip code input from the user and get the current
# By zipcode

# Define app as the __main__ Flask app
app = Flask(__name__, template_folder = 'templates')
app.config.from_object('config.DevelopmentConfig')

# Declare Form Classes
class CurrentTempForm(Form):
	zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
	submit = SubmitField('CHECK TEMPERATURE')

class ForcastForm(Form):
	zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
	submit = SubmitField('CHECK FORCAST')


# Templates is the standad directroy to place templates. The first place Flask checks for the proper template
# Layout.html is the base layout extended to all the other templates
@app.route('/layout')
def layout():
	return render_template('layout.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp_form', methods=['GET', 'POST'])
def temp_form():
	form = CurrentTempForm()
	if form.validate_on_submit():
		session['zipcode'] = form.zipcode.data
		return redirect(url_for('temp_output'))
	return render_template('temp_form.html', form=form)

@app.route('/temp_output', methods=['GET','POST'])
def temp_output():
	zipcode = session['zipcode']
	response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+'&APPID='APIKEY'')
	# Declaring the json object as the response of the API call in JSON format
	json_object = response.json()

	# Temperature in Kelvin is equal to the value of the temp key which is a subkey of the main key
	kelvin = float(json_object['main']['temp'])

	# Name is the JSON objext associated with the city/town name
	name = json_object['name']
	# Country is the JSON object associated with the Country
	country = json_object['sys']['country']
	# Formaula to convert temperature from Kelvin to fahrenheit
	# Decision structure to determine weather to round the float up or down
	fahrenheit = 1.8 * (kelvin - 273) + 32
	if fahrenheit > math.floor(fahrenheit) + 0.5:
		fahrenheit = math.ceil(fahrenheit)
	elif fahrenheit < math.floor(fahrenheit) + 0.5:
		fahrenheit = math.floor(fahrenheit)
	return render_template('temp_output.html',zipcode=zipcode, name=name, country=country, temp=fahrenheit)


@app.route('/forcast_form', methods=['GET', 'POST'])
def forcast_form():
	form = ForcastForm()
	if form.validate_on_submit():
		session['zipcode'] = form.zipcode.data
		return redirect(url_for('temp_graph'))
		
	return render_template('forcast_form.html', form=form)

@app.route('/graph', methods=['GET', 'POST'])
def temp_graph():
	zipcode = session['zipcode']
	response = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+'&APPID='APIKEY'')
	json_object = response.json()
	# Name is the JSON objext associated with the city/town name
	name = json_object['city']['name']
	# Country is the JSON object associated with the Country
	country = json_object['city']['country']

	def low_temp():
		lowList= []
		day = 0
	# Loop For the Temp Low
		for x in range(7):
			kelvin = float(json_object['list'][day]['main']['temp_min'])
			fahrenheit = 1.8 * (kelvin - 273) + 32
			lowList.append(float(format(fahrenheit,'.2f')))
			day += 1
		return lowList

	def high_temp():
		day = 0
		highList = []
		for x in range(7):
			kelvin = float(json_object['list'][day]['main']['temp_max'])
			fahrenheit = 1.8 * (kelvin - 273) + 32
			highList.append(float(format(fahrenheit,'.2f')))
			day += 1
		return highList

	def wind_speed():
		day = 0
		windList = []
		for x in range(7):
			wind = json_object['list'][day]['wind']['speed']
			windList.append(wind)
			day += 1
		return windList

	wind = wind_speed()
	highs = high_temp()
	lows = low_temp()

	# Render the temp graph
	graph = pygal.Bar()
	graph.title = "7 Day Temperature Forcast"
	graph.x_labels = map(str, range(1, 8))
	graph.add('High Temp', highs)
	graph.add('Low Temp', lows)
	graph.add('Wind (km/h)', wind)
	graph.render()
	graph_data = graph.render_data_uri()
	return render_template('graph.html', zipcode=zipcode, city=name, country=country, graph_data=graph_data)

if __name__ == '__main__':
    app.run()
