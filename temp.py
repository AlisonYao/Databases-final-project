@app.route('/cusBuyTickets', methods=['GET', 'POST'])
def cusBuyTickets():
	if session.get('email'):
		email = session['email']
		db_email = check_apostrophe(email)
		airline_name = check_apostrophe(request.form['airline_name'])
		flight_num = request.form['flight_num']

		cursor = conn.cursor()
		# query = "SELECT ticket_id \
		# 		FROM flight NATURAL JOIN ticket \
		# 		WHERE flight_num = \'{}\' AND \
		# 			ticket_id NOT IN (SELECT ticket_id \
		# 								FROM flight NATURAL JOIN ticket NATURAL JOIN purchases)\
		# 			AND flight_num = \'{}\'"
		# there is no extra failsafe anymore 
		query = "SELECT * \
				FROM flight \
				WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0"
		cursor.execute(query.format(airline_name, flight_num))
		# cursor.execute(query.format(flight_num, flight_num))
		data = cursor.fetchall()
		cursor.close()

		if(data):
			cursor = conn.cursor()
			# calc the new ticket id = biggest id + 1
			cursor = conn.cursor()
			query_id = "SELECT ticket_id \
						FROM ticket \
						ORDER BY ticket_id DESC \
						LIMIT 1"
			cursor.execute(query_id)
			ticket_id_data = cursor.fetchone() # (74373,)
			new_ticket_id = int(ticket_id_data[0]) + 1
			# first insert into ticket
			ins1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
			cursor.execute(ins1.format(new_ticket_id, airline_name, flight_num))
			# then insert into purchases
			ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', NULL, CURDATE())"
			cursor.execute(ins.format(new_ticket_id, db_email))
			conn.commit()
			cursor.close()
			message1 = 'Ticket bought successfully!'
			return render_template('cusSearchPurchase.html', email = email, message1 = message1)
		else:
			error = 'No ticket'
			return render_template('cusSearchPurchase.html', error2=error, email = email, emailName=email.split('@')[0])
	else:
		session.clear()
		return render_template('404.html')
