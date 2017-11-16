zipcode = request.form['zip']
	# Declaring response a an HTTP Get request calling the weather API
	response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+'&APPID=bf226275d913f1c0881e2da6d71359da')

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

	# Render the temperature.html file and subsitute temp into the "temp" value placeholder
	return render_template('temperature.html', name=name, country=country,  temp=format(fahrenheit, '.0f'))