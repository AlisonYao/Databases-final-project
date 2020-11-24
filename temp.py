@app.route('/cusSpending', methods=['POST', 'GET'])
def cusSpending():
	email = session['email']
	# cursor = conn.cursor()
	# duration = request.form.get("duration")
	# if duration is None:
	# 	duration = "30"

	# query = 'select sum(ticket_price * 0.1), avg(ticket_price * 0.1), count(ticket_price * 0.1) from agent_commission where email = \'{}\' and (purchase_date between DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())'
	# cursor.execute(query.format(email, duration))
	# commission_data = cursor.fetchone()
	# total_com, avg_com, count_ticket = commission_data
	# cursor.close()
	return render_template('cusSpending.html', email=email)
