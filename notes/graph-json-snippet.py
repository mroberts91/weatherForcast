@app.route('/graph', methods=['GET', 'POST'])
def temp_graph():
	dayList= []
	zipcode = request.form['zipcode']
	response = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+'&APPID=bf226275d913f1c0881e2da6d71359da')
	json_object = response.json()
	dayOne = json_object['list'][0]['main']['temp']
	dayTwo = json_object['list'][1]['main']['temp']
	dayThree = json_object['list'][2]['main']['temp']
	dayFour = json_object['list'][3]['main']['temp']
	dayFive = json_object['list'][4]['main']['temp']
	daySix = json_object['list'][5]['main']['temp']
	daySeven = json_object['list'][6]['main']['temp']
	return render_template('graph.html', one=dayOne, two=dayTwo, three=dayThree, four=dayFour, five=dayFive, six=daySix, seven=daySeven)
