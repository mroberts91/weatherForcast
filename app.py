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
# Form for the zipcode input on the temp_form template
class CurrentTempForm(Form):
	zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
	submit = SubmitField('CHECK TEMPERATURE')

# Class for the zipcode input on the forcast_form template
class ForcastForm(Form):
	zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
	submit = SubmitField('CHECK FORCAST')


# Layout.html is the base layout HTML template extended to all the other templates
# To provide unformed headers and footers and base HTML container on all pages
@app.route('/layout')
def layout():
	return render_template('layout.html')

# Route and rendering of the homepage, index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route and rendering of the current temperatur form HTMl page.
# Validating the form on submit for to have 5 characters
@app.route('/temp_form', methods=['GET', 'POST'])
def temp_form():
	form = CurrentTempForm()
	if form.validate_on_submit():
		# Storing the zipcode entered by the user as a session variable
		# Found that storing it as a session variable was easier when trying to recieve the variable for the API/
			# call on the temp output api call.
		session['zipcode'] = form.zipcode.data
		# When the form is submited, redirect to the temp_output HTML template
		return redirect(url_for('temp_output'))
	# On intial page load render the forcat_form HTML
	return render_template('temp_form.html', form=form)


# Route and rendering out the Current Temperature Display Page
# Recieves the session variable 'zipcode' and calls the API using the zipcode entered by the user
@app.route('/temp_output', methods=['GET','POST'])
def temp_output():
	zipcode = session['zipcode']
	# Calling the OWM API and getting the JSON response from the API
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


# Flask route and rendering of the forcast_form HTMl page
# Calling the Form class and validating the user input for lenght
# Stored the user input as a session variable 'zipcode'
@app.route('/forcast_form', methods=['GET', 'POST'])
def forcast_form():
	form = ForcastForm()
	if form.validate_on_submit():
		session['zipcode'] = form.zipcode.data
		# When the form is submitted redirect to the graph HTML template
		return redirect(url_for('temp_graph'))
	# On intial page load render the forcat_form HTML
	return render_template('forcast_form.html', form=form)


# Flaks route and rendering of the graph HTML page
@app.route('/graph', methods=['GET', 'POST'])
def temp_graph():
	zipcode = session['zipcode']
	# Call the API using the user input on the forcast_form template
	response = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+'&APPID='APIKEY'')
	# The response in the JSON returned by the API call
	json_object = response.json()
	# Name is the JSON objext associated with the city/town name
	name = json_object['city']['name']
	# Country is the JSON object associated with the Country
	country = json_object['city']['country']

	# Creating the list of data points for the low temperature forcast
	def low_temp():
		lowList= []
		day = 0
	# Iterate through the JSON response for each day in the JSON file, get the min temp
		# and append the data into the low temp list
		for x in range(7):
			kelvin = float(json_object['list'][day]['main']['temp_min'])
			# convert kelvin to fahrenheit
			fahrenheit = 1.8 * (kelvin - 273) + 32
			lowList.append(float(format(fahrenheit,'.2f')))
			day += 1
		return lowList

	def high_temp():
		day = 0
		highList = []
	# Iterate through the JSON response for each day in the JSON file, get the max temp
		# and append the data into the high temp list
		for x in range(7):
			kelvin = float(json_object['list'][day]['main']['temp_max'])
			fahrenheit = 1.8 * (kelvin - 273) + 32
			highList.append(float(format(fahrenheit,'.2f')))
			day += 1
		return highList

	def wind_speed():
		day = 0
		windList = []
	# Iterate through the JSON response for each day in the JSON file, get the wind speed
		# and append the data into the wind speed list
		for x in range(5):
			wind = json_object['list'][day]['wind']['speed']
			windList.append(wind)
			day += 1
		return windList

	wind = wind_speed()
	highs = high_temp()
	lows = low_temp()

	# Render the temp graph using the lists created earlier as data points for the graph
	graph = pygal.Bar()
	graph.title = "7 Day Temperature Forcast"
	graph.x_labels = map(str, range(1, 6))
	graph.add('High Temp', highs)
	graph.add('Low Temp', lows)
	graph.add('Wind (km/h)', wind)
	graph.render()
	graph_data = graph.render_data_uri()
	return render_template('graph.html', zipcode=zipcode, city=name, country=country, graph_data=graph_data)


# Flask routes to dispay the error and render the error HTML template
# Display the error that occured
# error HTML also has the layout.html extension
@app.errorhandler(KeyError)
@app.errorhandler(400)
@app.errorhandler(500)
@app.errorhandler(404)
def runtime_error(e):
	return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run()
