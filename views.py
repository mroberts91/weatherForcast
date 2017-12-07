from flask import Flask, render_template, url_for, redirect, session
from sqlalchemy import create_engine
import pandas as pd
import pygal
import requests
import math
from forms import *

main = Flask(__name__)
main.config.from_object('config.DevelopmentConfig')

# Creating SQLAlchemy Engine
engine = create_engine("sqlite:///c:/Users/micha/Documents/Development/weatherWebApp/zip_code_data.db")


# Route and rendering of the homepage, index.html
@main.route('/')
def index():
    return render_template('index.html')

# View to lookup a zipcode by city and state
# Using sqlalchemy and pandas to query the database and create a DataFrame from the query results
# Once pandas has generated the DataFrame, the DataFrame is rendered into a HTML table and displayed
@main.route('/lookup', methods=['GET', 'POST'])
def lookup_form():
    form = LookupForm()
    if form.validate_on_submit():
        entered = form.cityName.data.title()
        nameData = entered.replace("St.", "Saint")
        city = "'" + nameData + "'"
        stateData = form.stateName.data
        abbr = "'" + stateData + "'"
        if form.cityName.data:
            df = pd.read_sql_query(f"SELECT * FROM city_data WHERE City={city} and Abbr={abbr}", engine)
        if len(form.cityName.data) < 1:
            df = pd.read_sql_query(f"SELECT * FROM city_data WHERE Abbr={abbr}", engine)
        if len(df) == 0:
            letters = "'" + nameData + "%" + "'"
            df = pd.read_sql_query(f"SELECT * FROM city_data WHERE City LIKE {letters} AND Abbr={abbr}", engine)
        df.set_index("Zipcode", inplace=True)
        table = df.to_html()
        return render_template('lookup.html', form=form, table=table)
    return render_template('lookup.html', form=form)


# Route and rendering of the current temperatur form HTMl page.
# Validating the form on submit for to have 5 characters
@main.route('/temp_form', methods=['GET', 'POST'])
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
@main.route('/temp_output', methods=['GET', 'POST'])
def temp_output():
    zipcode = session['zipcode']
    # Calling the OWM API and getting the JSON response from the API
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + '&APPID=bf226275d913f1c0881e2da6d71359da')
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
    return render_template('temp_output.html', zipcode=zipcode, name=name, country=country, temp=fahrenheit)


# Flask route and rendering of the forcast_form HTMl page
# Calling the Form class and validating the user input for lenght
# Stored the user input as a session variable 'zipcode'
@main.route('/forcast_form', methods=['GET', 'POST'])
def forcast_form():
    form = ForcastForm()
    if form.validate_on_submit():
        session['zipcode'] = form.zipcode.data
        # When the form is submitted redirect to the graph HTML template
        return redirect(url_for('temp_graph'))
    # On intial page load render the forcat_form HTML
    return render_template('forcast_form.html', form=form)


# Flaks route and rendering of the graph HTML page
@main.route('/graph', methods=['GET', 'POST'])
def temp_graph():
    zipcode = session['zipcode']
    # Call the API using the user input on the forcast_form template
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip=' + zipcode + '&APPID=bf226275d913f1c0881e2da6d71359da')
    # The response in the JSON returned by the API call
    json_object = response.json()
    # Name is the JSON objext associated with the city/town name
    name = json_object['city']['name']
    # Country is the JSON object associated with the Country
    country = json_object['city']['country']

    # Creating the list of data points for the low temperature forcast
    def low_temp():
        lowList = []
        day = 0
    # Iterate through the JSON response for each day in the JSON file, get the min temp
        # and append the data into the low temp list
        for x in range(7):
            kelvin = float(json_object['list'][day]['main']['temp_min'])
            # convert kelvin to fahrenheit
            fahrenheit = 1.8 * (kelvin - 273) + 32
            lowList.append(float(format(fahrenheit, '.2f')))
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
            highList.append(float(format(fahrenheit, '.2f')))
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

@main.errorhandler(400)
@main.errorhandler(500)
@main.errorhandler(404)
def runtime_error(e):
    return render_template('error.html', error=str(e))


if __name__ == '__main__':
    main.run()
