@app.route('/map')
def map():
	response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=29576&APPID=bf226275d913f1c0881e2da6d71359da')

	# Declaring the json object as the response of the API call in JSON format
	json_object = response.json()

	# Temperature in Kelvin is equal to the value of the temp key which is a subkey of the main key
	kelvin = float(json_object['main']['temp'])

	sndmap = Map(
	        identifier="sndmap",
	        lat=33.55,
	        lng=-79.04,
	        maptype="HYBRID",
	        zoom=9,
	        style=None,
	        markers=[
	          	{
		             'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
		             'lat': 33.55,
		             'lng': -79.04,
		             'infobox': "<b>Hello World</b>"
	          	}
	      	]
	    )
	return render_template('map.html', sndmap=sndmap, kelvin=kelvin)