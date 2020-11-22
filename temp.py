@app.route('/agentSearchFlight', methods=['GET', 'POST'])
def agentSearchFlight():
	email = session['email']
	departure_city = request.form['departure_city']
	departure_airport = request.form['departure_airport']
	arrival_city = request.form['arrival_city']
	arrival_airport = request.form['arrival_airport']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	# validate booking agent email
	cursor = conn.cursor()
	query = " select booking_agent_id from booking_agent where email = \'{}\'"
	cursor.execute(query.format(email))
	agent_data = cursor.fetchone() # tuple (98765,)
	booking_agent_id = agent_data[0]
	cursor.close()

	if not (agent_data):
		agent_id_error = 'You are not a booking agent'
		return render_template('agentSearchPurchase.html', error1=agent_id_error)

	# booking agent email validated
	cursor = conn.cursor()
	query = "SELECT airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status, price \
				FROM airport as D, flight, airport AS A \
				WHERE D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\') and \
				D.airport_name = departure_airport and \
				departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
				A.airport_city = if (\'{}\' = '', A.airport_city, \'{}\')and \
				A.airport_name = arrival_airport and \
				arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\')and \
				date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\')and \
				date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\')"
	cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date, arrival_date))
	data = cursor.fetchall()
	
	error = None
	if (data): # has data
		return render_template('agentSearchPurchase.html', email=email, upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('agentSearchPurchase.html', email=email, error1=error)
