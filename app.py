# NOTE: temp.py is just for debuging and testing py file. Just personal habit. The file is not important. 
# NOTE-Cheryl: I have created new views, plz refer to DB_for_testing/create_view
# also commission is spelled with 2 s's (Ive fixed it)
# there is a typo somewhere that says creat instead of create (I fixed the ones I have found)
# TODO-both: check SQL after everything is finished. View & Grant
# TODO-both: Cross check each other's work
# BUG-Cheryl: datediff(CURDATE(), DATE(purchase_date)) should have CURDATE() as first arg, or your datediff is a negative number and is always < 30
# TODO-Cheryl: Plz refer to agent page for inspiration lol
# BUG-Cheryl: most of cus does not work for me why
# TODO-Alison: prettier tables??

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
# conn = mysql.connector.connect(host='localhost',
#                        user='root',
#                        password='86466491@Alison',
#                        database='temp')

conn = mysql.connector.connect(host='localhost',
                       user='root',
                       password='root',
                       database='air')

#####################################################################
#                               PUBLIC                              #
#                all operations from the public side                #
#####################################################################
@app.route('/')
def publicHome():
	return render_template('publicHome.html')

# TODO-Alison: why is the freaking view not working????? space & tab problems?????
@app.route('/publicSearchFlight', methods=['GET', 'POST'])
def publicSearchFlight():
    departure_city = request.form['departure_city']
    departure_airport = request.form['departure_airport']
    arrival_city = request.form['arrival_city']
    arrival_airport = request.form['arrival_airport']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']

    cursor = conn.cursor()
	# query = "select * \
	# 		from public_search_flight \
    #         where departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
	# 			arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') and \
	# 			status = 'upcoming' and \
	# 			departure_city = if (\'{}\' = '', departure_city, \'{}\') and \
	# 			arrival_city = if (\'{}\' = '', arrival_city, \'{}\') and \
    #         	date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') and \
	# 			date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\')"
    query = "select * \
            from airport as D, flight, airport as A \
            where D.airport_name = flight.departure_airport and flight.arrival_airport = A.airport_name and \
            D.airport_name = if (\'{}\' = '',D.airport_name, \'{}\') and \
				A.airport_name = if (\'{}\' = '',A.airport_name, \'{}\') and \
					flight.status = 'upcoming' and \
			D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\')\
				 and A.airport_city = if (\'{}\' = '',A.airport_city, \'{}\') and \
            date(flight.departure_time) = if (\'{}\' = '',date(flight.departure_time), \'{}\')\
				 and date(flight.arrival_time) = if (\'{}\' = '',date(flight.arrival_time), \'{}\')"
    cursor.execute(query.format(departure_airport, departure_airport, \
		arrival_airport, arrival_airport, \
			departure_city, departure_city,\
				arrival_city, arrival_city,\
					departure_date, departure_date,\
						arrival_date, arrival_date))
    data = cursor.fetchall() 
    cursor.close()
    
    error = None
    if (data): # has data
        return render_template('publicHome.html', upcoming_flights=data)
    else: # does not have data
        error = 'Sorry ... Cannot find this flight!'
        return render_template('publicHome.html', error1=error)

@app.route('/publicSearchStatus', methods=['GET', 'POST'])
def publicSearchStatus():
    flight_num = request.form['flight_num']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']

    cursor = conn.cursor()
    query = "select * \
            from flight \
            where flight_num = \'{}\' \
                and date(departure_time) = \'{}\' \
                and date(arrival_time) = \'{}\'"
    cursor.execute(query.format(flight_num, arrival_date, departure_date))
    data = cursor.fetchall() 
    cursor.close()
    
    error = None
    if (data): # has data
        return render_template('publicHome.html', statuses=data)
    else: # does not have data
        error = 'Sorry ... Cannot find this flight!'
        return render_template('publicHome.html', error2=error)


#####################################################################
#                              CUSTOMER                             #
#               all operations from the customer side               #
#####################################################################
#Define route for login
@app.route('/cuslogin')
def cuslogin():
	return render_template('cuslogin.html')

#Define route for register
@app.route('/cusregister')
def cusregister():
	return render_template('cusregister.html')

#Authenticates the login
@app.route('/cusloginAuth', methods=['GET', 'POST'])
def cusloginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT email, password FROM customer WHERE email = \'{}\' and password = \'{}\'"
	cursor.execute(query.format(email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('cushome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('cuslogin.html', error=error)

#Authenticates the register
@app.route('/cusregisterAuth', methods=['GET', 'POST'])
def cusregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email = \'{}\'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('cusregister.html', error = error)
	else:
		ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		flash("You are logged in")
		session['email'] = email
		return redirect(url_for('cushome'))

@app.route('/cushome')
def cushome():
    email = session['email']
    cursor = conn.cursor()
    query = "SELECT ticket_id, airline_name, airplane_id, flight_num, \
		D.airport_city, \
		departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
			FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
				 WHERE customer_email = \'{}\' and status = 'upcoming' and \
				D.airport_name = departure_airport and A.airport_name = arrival_airport"
    cursor.execute(query.format(email))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('cushome.html', email=email, view_my_flights=data1)

@app.route('/cusSearchPurchase')
def cusSearchPurchase():
	email = session['email'] 
	return render_template('cusSearchPurchase.html', email=email)

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

@app.route('/cusSearchFlight', methods=['GET', 'POST'])
def cusSearchFlight():
	email = session['email']
	departure_city = request.form['departure_city']
	departure_airport = request.form['departure_airport']
	arrival_city = request.form['arrival_city']
	arrival_airport = request.form['arrival_airport']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	status = request.form['status']
	# username = session['username']

	cursor = conn.cursor()
	# query = "SELECT airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, \
	# 		status, price\
	# 	FROM airport as D, flight NATRUAL JOIN airline_staff, airport AS A WHERE \
	# 	D.airport_city = \'{}\' and \
	# 	D.airport_name = departure_airport and \
	# 	departure_airport = \'{}\' and \
	# 	A.airport_city = \'{}\'and \
	# 	A.airport_name = arrival_airport and \
	# 	arrival_airport =  \'{}\' and \
    #     date(departure_time) = \'{}\' and \
	# 	date(arrival_time) =  \'{}\' and \
	# 	username = \'{}\'"
	query = "SELECT airline_name, airplane_id, flight_num, D.airport_city, departure_airport, \
		A.airport_city, arrival_airport, departure_time, arrival_time, \
			status, price, count(ticket_id)\
		FROM airport as D, flight NATURAL JOIN ticket, airport AS A WHERE \
		D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\') and \
		D.airport_name = departure_airport and \
		departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
		A.airport_city = if (\'{}\' = '', A.airport_city, \'{}\')and \
		A.airport_name = arrival_airport and \
		arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\')and \
        date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\')and \
		date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\') and \
		status =  if (\'{}\' = '', status, \'{}\') and \
		ticket_id NOT IN (SELECT ticket_id FROM flight NATURAL JOIN ticket NATURAL JOIN purchases) \
		GROUP BY airline_name, airplane_id, flight_num, D.airport_city, departure_airport, \
		A.airport_city, arrival_airport, departure_time, arrival_time, \
			status, price"

	# cursor.execute(query.format(departure_city, departure_airport, arrival_city, arrival_airport, departure_date, arrival_date,username))
	cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, \
		arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, \
			arrival_date,arrival_date, status, status))
	# cursor.execute(query)
	data = cursor.fetchall()

	cursor.close()
    
	error = None
	if (data): # has data
		cursor = conn.cursor()
		query = "SELECT airline_name, airplane_id, flight_num, D.airport_city,\
		departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
		FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A \
			WHERE customer_email = \'{}\' and status = 'upcoming' and \
				D.airport_name = departure_airport and A.airport_name = arrival_airport"
		cursor.execute(query.format(email))
		data1 = cursor.fetchall() 
		cursor.close()

		return render_template('cushome.html',email = email, upcoming_flights=data, posts = data1)
		# return redirect(url_for('cushome'), upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('cushome.html',email = email, error1=error)	

@app.route('/cus_buy_ticket', methods=['GET', 'POST'])
def cus_buy_ticket():
	email = session['email']
	# email = request.form['email']
	flight_num = request.form['flight_num']
	cursor = conn.cursor()
	query = "SELECT ticket_id FROM flight NATURAL JOIN ticket\
	WHERE flight_num = \'{}\' \
		AND ticket_id NOT IN (SELECT ticket_id FROM flight NATURAL JOIN ticket NATURAL JOIN purchases)\
	AND flight_num = \'{}\'"
	cursor.execute(query.format(flight_num, flight_num))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	# error2 = None

	if(data):
		# email = session['email']
		#creates a session for the the user
		#session is a built in
		cursor = conn.cursor()
		ticket = int(data[0][0])
		ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', NULL, CURDATE())"
		cursor.execute(ins.format(ticket, email))
		# cursor.execute(query.format(email))
		conn.commit()
		cursor.close()
		
		return redirect(url_for('cushome'))
	else:
		#returns an error message to the html page
		error = 'No ticket left'
		cursor = conn.cursor()
		query = "SELECT ticket_id, airline_name, airplane_id, flight_num, \
		D.airport_city, \
		departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
			FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
				 WHERE customer_email = \'{}\' and status = 'upcoming' and \
				D.airport_name = departure_airport and A.airport_name = arrival_airport"
		cursor.execute(query.format(email))
		data1 = cursor.fetchall() 
		cursor.close()
		return render_template('cushome.html', error2=error, email = email, posts = data1)
	#executes query
	# ins = "INSERT INTO purchases VALUES (NULL, \'{}\', CURDATE(), ticket_id\
	# WHERE flight_number = "
	# cursor.execute(ins.format(email))
	# conn.commit()
	# cursor.close()
	# return redirect(url_for('cushome'))	


#####################################################################
#                         BOOKING AGENT                             #
#            all operations from the booking_agent side             #
#####################################################################
@app.route('/agentlogin')
def agentlogin():
	return render_template('agentlogin.html')

@app.route('/agentregister')
def agentregister():
	return render_template('agentregister.html')

@app.route('/agentloginAuth', methods=['GET', 'POST'])
def agentloginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT email, password FROM booking_agent WHERE email = \'{}\' and password = \'{}\'"
	cursor.execute(query.format(email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		email = request.form['email']
		# get view_my_flights info from db
		cursor = conn.cursor()
		query = "SELECT * FROM agent_viewmyflight WHERE email = \'{}\'"
		cursor.execute(query.format(email))
		data2 = cursor.fetchall()
		cursor.close()
		session['email'] = email
		# return redirect(url_for('agentHome', email=email, view_my_flights=data2))
		return render_template('agenthome.html', email=email, view_my_flights=data2)
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('agentlogin.html', error=error)

@app.route('/agentregisterAuth', methods=['GET', 'POST'])
def agentregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('agentregister.html', error = error)
	else:
		ins = "INSERT INTO booking_agent VALUES(\'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(email, password, booking_agent_id))
		conn.commit()
		# get view_my_flights info from db
		query = "SELECT * FROM agent_viewMyFlight WHERE email = \'{}\'"
		cursor.execute(query.format(email))
		data2 = cursor.fetchall()
		cursor.close()
		session['email'] = email
		flash("You are logged in")
		return render_template('agenthome.html', email=email, view_my_flights=data2)

@app.route('/agentHome')
def agentHome():
	email = session['email']
	cursor = conn.cursor()
	query = "SELECT * FROM agent_viewmyflight WHERE email = \'{}\'"
	cursor.execute(query.format(email))
	data2 = cursor.fetchall()
	cursor.close()
	return render_template('agenthome.html', email=email, view_my_flights=data2)

@app.route('/agentSearchPurchase')
def agentSearchPurchase():
	email = session['email'] 
	return render_template('agentSearchPurchase.html', email=email)

@app.route('/agentCommission', methods=['POST', 'GET'])
def agentCommission():
	email = session['email']
	cursor = conn.cursor()
	duration = request.form.get("duration")
	if duration is None:
		duration = "30"

	query = 'select sum(ticket_price * 0.1), avg(ticket_price * 0.1), count(ticket_price * 0.1) from agent_commission where email = \'{}\' and (purchase_date between DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())'
	cursor.execute(query.format(email, duration))
	commission_data = cursor.fetchone()
	total_com, avg_com, count_ticket = commission_data
	cursor.close()
	return render_template('agentCommission.html', email=email, total_com=total_com, avg_com=avg_com, count_ticket=count_ticket, duration=duration)

@app.route('/agentTopCustomers')
def agentTopCustomers():
	email = session['email']
	cursor = conn.cursor()
	query = "select customer_email, count(ticket_id) from agent_commission where email = \'{}\' and datediff(CURDATE(), DATE(purchase_date)) < 183 group by customer_email order by count(ticket_id) desc"
	cursor.execute(query.format(email))
	ticket_data = cursor.fetchall() # [('alison@gmail.com', 5), ('Alison1234@gmail.com', 2), ('clark@gmail.com', 1)]
	cursor.close()

	l = len(ticket_data)
	if l >= 5:
		ppl1 = [ticket_data[i][0] for i in range(5)]
		tickets = [ticket_data[i][1] for i in range(5)]
	else:
		ppl1 = [ticket_data[i][0] for i in range(l)]
		tickets = [ticket_data[i][1] for i in range(l)]
		for i in range(5 - l):
			ppl1.append(' ')
			tickets.append(0)
	
	cursor = conn.cursor()
	query2 = "select customer_email, sum(ticket_price) from agent_commission where email = \'{}\' and datediff(CURDATE(), DATE(purchase_date)) < 365 group by customer_email order by sum(ticket_price) desc"
	cursor.execute(query2.format(email))
	commission_data = cursor.fetchall()
	cursor.close()

	l2 = len(commission_data)
	if l2 >= 5:
		ppl2 = [commission_data[i][0] for i in range(5)]
		commissions = [commission_data[i][1] for i in range(5)]
	else:
		ppl2 = [commission_data[i][0] for i in range(l2)]
		commissions = [int(commission_data[i][1]) for i in range(l2)]
		for i in range(5 - l):
			ppl2.append(' ')
			commissions.append(0)

	print(commissions)
	return render_template('agentTopCustomers.html', email=email, ppl1=ppl1, ppl2=ppl2, tickets=tickets, commissions=commissions)

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
	
	if (data): # has data
		return render_template('agentSearchPurchase.html', email=email, upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('agentSearchPurchase.html', email=email, error1=error)

@app.route('/agentBuyTickets', methods=['GET', 'POST'])
def agentBuyTickets():
	email = session['email']
	flight_num = request.form.get("flight_num")
	customer_email = request.form['customer_email']

	# validate booking agent email
	cursor = conn.cursor()
	query = " select booking_agent_id from booking_agent where email = \'{}\'"
	cursor.execute(query.format(email))
	agent_data = cursor.fetchone() # tuple (98765,)
	booking_agent_id = agent_data[0]
	cursor.close()

	if not (agent_data):
		agent_id_error = 'You are not a booking agent'
		return render_template('agentSearchPurchase.html', error2=agent_id_error)

	# validate customer_email is registered
	cursor = conn.cursor()
	query = " select * from customer where email = \'{}\'"
	cursor.execute(query.format(customer_email))
	cus_data = cursor.fetchone()
	cursor.close()

	if not (cus_data):
		email_error = 'Your customer is not registered.'
		return render_template('agentSearchPurchase.html', error2=email_error)

	# customer_email is validated	
	cursor = conn.cursor()
	query = "SELECT ticket_id \
			FROM flight NATURAL JOIN ticket\
			WHERE flight_num = \'{}\' \
			AND ticket_id NOT IN (SELECT ticket_id \
									FROM flight NATURAL JOIN ticket NATURAL JOIN purchases)\
			AND flight_num = \'{}\'"
	cursor.execute(query.format(flight_num, flight_num))
	ticket_data = cursor.fetchall()
	cursor.close()

	if not (ticket_data):
		ticket_error = 'No ticket left'
		return render_template('agentSearchPurchase.html', error2=ticket_error, email=email)
	else:
		cursor = conn.cursor()
		ticket_id = int(ticket_data[0][0])
		ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', \'{}\', CURDATE())"
		cursor.execute(ins.format(ticket_id, customer_email, booking_agent_id))
		conn.commit()
		cursor.close()
		message = 'Ticket bought successfully!'
		return render_template('agentSearchPurchase.html', message=message, email=email)


#####################################################################
#                         AIRLINE STAFF                             #
#            all operations from the airlinr_staff side             #
#####################################################################
@app.route('/stafflogin')
def stafflogin():
	return render_template('stafflogin.html')

#Define route for register
@app.route('/staffregister')
def staffregister():
	return render_template('staffregister.html')

#Authenticates the login
@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT username, password FROM airline_staff WHERE username = \'{}\' and password = \'{}\'"
	cursor.execute(query.format(username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('staffhome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('stafflogin.html', error=error)

#Authenticates the register
@app.route('/staffregisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
	cursor.execute(query.format(username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staffregister.html', error = error)
	
	#executes query
	query = "SELECT airline_name FROM airline WHERE airline_name = \'{}\'"
	cursor.execute(query.format(airline_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	
	if(data):
		ins = "INSERT INTO airline_staff VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		flash("You are logged in")
		session['username'] = username
		return redirect(url_for('staffhome'))
	else:
		#If the previous query returns data, then user exists
		error = "This airline doesn't exist"
		cursor.close()
		return render_template('staffregister.html', error = error)

@app.route('/staffhome')
def staffhome():
	username = session['username']
    # airline_name = session['airline_name']
	cursor = conn.cursor();
	query = "SELECT airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight NATRUAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(DATE(departure_time), CURDATE()) < 30 "
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('staffhome.html', username=username, posts=data1)

@app.route('/staffSearchFlight', methods=['GET', 'POST'])
def staffSearchFlight():
	departure_city = request.form['departure_city']
	departure_airport = request.form['departure_airport']
	arrival_city = request.form['arrival_city']
	arrival_airport = request.form['arrival_airport']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	username = session['username']

	cursor = conn.cursor()
	# query = "SELECT airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, \
	# 		status, price\
	# 	FROM airport as D, flight NATRUAL JOIN airline_staff, airport AS A WHERE \
	# 	D.airport_city = \'{}\' and \
	# 	D.airport_name = departure_airport and \
	# 	departure_airport = \'{}\' and \
	# 	A.airport_city = \'{}\'and \
	# 	A.airport_name = arrival_airport and \
	# 	arrival_airport =  \'{}\' and \
    #     date(departure_time) = \'{}\' and \
	# 	date(arrival_time) =  \'{}\' and \
	# 	username = \'{}\'"
	query = "SELECT airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, \
			status, price\
		FROM airport as D, flight NATRUAL JOIN airline_staff, airport AS A WHERE \
		D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\') and \
		D.airport_name = departure_airport and \
		departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
		A.airport_city = if (\'{}\' = '', A.airport_city, \'{}\')and \
		A.airport_name = arrival_airport and \
		arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\')and \
        date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\')and \
		date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\') and \
		username = \'{}\'"

	# cursor.execute(query.format(departure_city, departure_airport, arrival_city, arrival_airport, departure_date, arrival_date,username))
	cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date,arrival_date,username))
	# cursor.execute(query)
	data = cursor.fetchall()

	query1 = "SELECT airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight NATRUAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(DATE(departure_time), CURDATE()) < 30 "
	cursor.execute(query1.format(username))
	data1 = cursor.fetchall()

	cursor.close()
    
	error = None
	if (data): # has data
		return render_template('staffhome.html', username=username, posts=data1, upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('staffhome.html', username=username, posts=data1, error1=error)

@app.route('/addinfo')
def addinfo():
	return render_template('addinfo.html')

@app.route('/edit_status', methods=['GET', 'POST'])
def edit_status():
	status = request.form['edit_status']

	flight_num = request.form['flight_num']
	
	cursor = conn.cursor()
	#executes query
	upd = "UPDATE flight set status = \'{}\' WHERE flight_num = \'{}\'"
	cursor.execute(upd.format(status, flight_num))
	conn.commit()
	cursor.close()
	return redirect(url_for('staffhome'))

@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
	username = session['username']
	#grabs information from the forms
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	departure_airport = request.form['departure_airport']
	departure_time = request.form['departure_time']
	arrival_airport = request.form['arrival_airport']
	arrival_time = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT airline_name, flight_num FROM flight WHERE airline_name = \'{}\' and flight_num = \'{}\'"
	cursor.execute(query.format(airline_name, flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This flight already exists"
		return render_template('addinfo.html', error = error)

	#executes query
	query = "SELECT username, airline_name FROM airline_staff WHERE username = \'{}\' and airline_name = \'{}\'"
	cursor.execute(query.format(username, airline_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	
	if(data):
		ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
		conn.commit()

		flash("New flight added")
		return render_template('addinfo.html', error = error)
	else:
		#If the previous query returns data, then user exists
		error = "Wrong airline"
		cursor.close()
		return render_template('addinfo.html', error = error)

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	username = session['username']
	#grabs information from the forms
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT airline_name, airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
	cursor.execute(query.format(airline_name, airplane_id))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airplane already exists"
		return render_template('addinfo.html', error = error)

	#executes query
	query = "SELECT username, airline_name FROM airline_staff WHERE username = \'{}\' and airline_name = \'{}\'"
	cursor.execute(query.format(username, airline_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	
	if(data):
		ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(airline_name, airplane_id, seats))
		conn.commit()

		flash("New airplane added")
		return render_template('addinfo.html', error = error)
	else:
		#If the previous query returns data, then user exists
		error = "Wrong airline"
		cursor.close()
		return render_template('addinfo.html', error = error)

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	username = session['username']
	#grabs information from the forms
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_city']
	# seats = request.form['seats']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT airport_name FROM airport"
	cursor.execute(query.format(airport_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airport already exists"
		return render_template('addinfo.html', error = error)

	else:
		ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\')"
		cursor.execute(ins.format(airport_name, airport_city))
		conn.commit()

		flash("New airport added")
		return render_template('addinfo.html', error = error)

@app.route('/staffagent')
def staffagent():
	# username = session['username']
    # airline_name = session['airline_name']
	cursor = conn.cursor();
	query1 = "SELECT email, booking_agent_id, count(customer_email) as commission FROM booking_agent NATURAL JOIN purchases \
		WHERE YEAR(purchase_date) =  YEAR(CURDATE()) - 1  \
			GROUP BY email, booking_agent_id \
				ORDER BY commission DESC\
					LIMIT 5 "
	# cursor.execute(query.format(username))
	cursor.execute(query1)
	data1 = cursor.fetchall()

	cursor = conn.cursor();
	query2 = "SELECT email, booking_agent_id, sum(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchases \
		WHERE MONTH(purchase_date) =  MONTH(CURDATE()) - 1 \
			GROUP BY email, booking_agent_id \
				ORDER BY ticket DESC LIMIT 5 "
	# cursor.execute(query.format(username))
	cursor.execute(query2)
	data2 = cursor.fetchall()

	cursor = conn.cursor();
	query3 = "SELECT email, booking_agent_id, sum(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchases \
		WHERE YEAR(purchase_date) =  YEAR(CURDATE()) - 1 \
			GROUP BY email, booking_agent_id \
				ORDER BY ticket DESC LIMIT 5 "
	# cursor.execute(query.format(username))
	cursor.execute(query3)
	data3 = cursor.fetchall()

	cursor = conn.cursor();
	query = "SELECT * FROM booking_agent"
	# cursor.execute(query.format(username))
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	# return render_template('staffhome.html', username=username, posts=data1)
	return render_template('staffagent.html', commission = data1, month = data2, year = data3, posts = data)

# @app.route('/edit_status', methods=['GET', 'POST'])
# def edit_status():
# 	status = request.form['edit_status']

# 	flight_num = request.form['flight_num']
	
# 	cursor = conn.cursor()
# 	#executes query
# 	upd = "UPDATE flight set status = \'{}\' WHERE flight_num = \'{}\'"
# 	cursor.execute(upd.format(status, flight_num))
# 	conn.commit()
# 	cursor.close()
# 	return redirect(url_for('staffhome'))

@app.route('/staffcus')
def staffcus():
	username = session['username']
    # airline_name = session['airline_name']
	cursor = conn.cursor();
	query1 = "SELECT email, name FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY count(ticket_id) LIMIT 1"
	cursor.execute(query1.format(username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('staffcus.html', frequent = data1)

	# cursor = conn.cursor();

@app.route('/staffcusflight', methods=['GET', 'POST'])
def staffcusflight():
	username = session['username']
	email = request.form['customer_email']
	cursor = conn.cursor();
	query2 = "SELECT DISTINCT airplane_id, flight_num, \
		departure_airport, arrival_airport, departure_time, arrival_time, \
			status FROM customer, \
				purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE email = \'{}\' and email = customer_email and username = \'{}\'"
	cursor.execute(query2.format(email, username))
	# cursor.execute(query2)
	data2 = cursor.fetchall()

	query1 = "SELECT email, name FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY count(ticket_id) LIMIT 1"
	cursor.execute(query1.format(username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()

	cursor.close()
	error = None
	if(data2):
		return render_template('staffcus.html', cusflight = data2, frequent = data1)
	else:
		error = "No flight"
		# cursor.close()
		return render_template('staffcus.html', error = error, frequent = data1)
	# 

@app.route('/staffflightcus', methods=['GET', 'POST'])
def staffflightcus():
	username = session['username']
	flight = request.form['flight_num']
	cursor = conn.cursor();
	query3 = "SELECT DISTINCT email, name FROM customer, \
				purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE flight_num = \'{}\' and email = customer_email and username = \'{}\'"
	cursor.execute(query3.format(flight, username))
	# cursor.execute(query2)
	data3 = cursor.fetchall()

	query1 = "SELECT email, name \
		FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY count(ticket_id) LIMIT 1"
	cursor.execute(query1.format(username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()

	cursor.close()
	error3 = None
	if(data3):
		return render_template('staffcus.html', flightcus = data3, frequent = data1)
	else:
		error3 = "No customer"
		# cursor.close()
		return render_template('staffcus.html', error = error3, frequent = data1)
	
@app.route('/staffreport')
def staffreport():
	# username = session['username']
    # # airline_name = session['airline_name']
	cursor = conn.cursor();
	query1 = "SELECT airport_city FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and MONTH(purchase_date) >  MONTH(CURDATE()) - 3\
		GROUP BY airport_city\
		ORDER BY count(ticket_id) LIMIT 3"
	cursor.execute(query1)
	# cursor.execute(query1)
	month = cursor.fetchall()

	cursor = conn.cursor();
	query2 = "SELECT airport_city FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and YEAR(purchase_date) =  YEAR(CURDATE()) - 1\
			GROUP BY airport_city\
		ORDER BY count(ticket_id) LIMIT 3"
	cursor.execute(query2)
	# cursor.execute(query1)
	year = cursor.fetchall()

	cursor.close()
	return render_template('staffreport.html', month = month, year = year)

@app.route('/staffticket', methods=['GET', 'POST'])
def staffticket():
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor();
	ticket = "SELECT count(ticket_id) FROM \
			purchases NATURAL JOIN airline_staff NATURAL JOIN flight NATURAL JOIN ticket\
			WHERE purchase_date > \'{}\'  \
			and purchase_date < \'{}\'\
			GROUP BY airline_name"
	cursor.execute(ticket.format(start, end))
	# cursor.execute(query2)
	allticket = cursor.fetchall()

	query1 = "SELECT airport_city FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and MONTH(purchase_date) >  MONTH(CURDATE()) - 3\
		GROUP BY airport_city\
		ORDER BY count(ticket_id) LIMIT 3"
	cursor.execute(query1)
	# cursor.execute(query1)
	month = cursor.fetchall()

	cursor = conn.cursor();
	query2 = "SELECT airport_city FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and YEAR(purchase_date) =  YEAR(CURDATE()) - 1\
			GROUP BY airport_city\
		ORDER BY count(ticket_id) LIMIT 3"
	cursor.execute(query2)
	# cursor.execute(query1)
	year = cursor.fetchall()

	cursor.close()
	error = None
	if(allticket):
		return render_template('staffreport.html', allticket = allticket, month = month, year = year)
	else:
		error = "No ticket sold"
		# cursor.close()
		return render_template('staffreport.html', error = error, month = month, year = year)


#####################################################################
#                             COMMON                                #
#                   all operations from all sides                   #
#####################################################################
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/cuslogin')

@app.route('/logoutEmail')
def logoutEmail():
	session.pop('email')
	return redirect('/cuslogin')

# @app.route('/post', methods=['GET', 'POST'])
# def post():
# 	username = session['username']
# 	cursor = conn.cursor()
# 	blog = request.form['blog']
# 	query = "INSERT INTO blog (blog_post, username) VALUES(\'{}\', \'{}\')"
# 	cursor.execute(query.format(blog, username))
# 	conn.commit()
# 	cursor.close()
# 	return redirect(url_for('cushome'))

# @app.route('/logout')
# def logout():
# 	session.pop('email')
# 	return redirect('/')

# @app.route('/agenthome')
# def home():
    
#     username = session['username']
#     cursor = conn.cursor()
#     query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
#     cursor.execute(query.format(username))
#     data1 = cursor.fetchall() 
#     cursor.close()
#     return render_template('home.html', username=username, posts=data1)

		
# @app.route('/post', methods=['GET', 'POST'])
# def post():
# 	username = session['username']
# 	cursor = conn.cursor()
# 	blog = request.form['blog']
# 	query = "INSERT INTO blog (blog_post, username) VALUES(\'{}\', \'{}\')"
# 	cursor.execute(query.format(blog, username))
# 	conn.commit()
# 	cursor.close()
# 	return redirect(url_for('home'))

# @app.route('/logout')
# def logout():
# 	session.pop('username')
# 	return redirect('/')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
