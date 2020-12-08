from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector
import datetime
import json
import decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,decimal.Decimal):
            return float(o)
        super(DecimalEncoder,self).default(o)

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                       user='root',
                       password='86466491@Alison',
                       database='air')

# conn = mysql.connector.connect(host='localhost',
# 					   user='root',
# 					   password='root',
# 					   database='air')

#####################################################################
#                               HELPER                              #
#####################################################################
# for natural cases such as Dylan O'Brian and malicious cases such as inputing 2' or '1'='1 on purpose
# add a ' after every ' to escape so that SQL will not have any error
def check_apostrophe(x):
	assert type(x) == str
	if "'" not in x:
		return x
	db_x = ''
	for i in x:
		if i == "'":
			db_x += "''"
		else:
			db_x += i
	return db_x


#####################################################################
#                               PUBLIC                              #
#                all operations from the public side                #
#####################################################################
@app.route('/')
def publicHome():
	return render_template('publicHome.html')

@app.route('/publicSearchFlight', methods=['GET', 'POST'])
def publicSearchFlight():
	departure_city = check_apostrophe(request.form['departure_city'])
	departure_airport = check_apostrophe(request.form['departure_airport'])
	arrival_city = check_apostrophe(request.form['arrival_city'])
	arrival_airport = check_apostrophe(request.form['arrival_airport'])
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	cursor = conn.cursor()
	query = "select airline_name, flight_num, departure_city, departure_airport, departure_time, arrival_city, arrival_airport, arrival_time, price, airplane_id \
			from public_search_flight \
			where departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
					arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') and \
					status = 'upcoming' and \
					departure_city = if (\'{}\' = '', departure_city, \'{}\') and \
					arrival_city = if (\'{}\' = '',arrival_city, \'{}\') and \
					date(departure_time) = if (\'{}\' = '',date(departure_time), \'{}\') and \
					date(arrival_time) = if (\'{}\' = '',date(arrival_time), \'{}\')"
	cursor.execute(query.format(departure_airport, departure_airport, arrival_airport, arrival_airport, departure_city, departure_city, arrival_city, arrival_city, departure_date, departure_date, arrival_date, arrival_date))
	data = cursor.fetchall() 
	cursor.close()
	
	if (data): # has data
		return render_template('publicHome.html', upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('publicHome.html', error1=error)

@app.route('/publicSearchStatus', methods=['GET', 'POST'])
def publicSearchStatus():
	airline_name = check_apostrophe(request.form['airline_name'])
	flight_num = request.form['flight_num']
	arrival_date = request.form['arrival_date']
	departure_date = request.form['departure_date']

	cursor = conn.cursor()
	query = "select * \
			from public_search_flight \
			where flight_num = if (\'{}\' = '', flight_num, \'{}\') and \
					date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') and \
					date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') and \
					airline_name = if (\'{}\' = '', airline_name, \'{}\')"
	cursor.execute(query.format(flight_num, flight_num, arrival_date, arrival_date, departure_date, departure_date, airline_name, airline_name))
	data = cursor.fetchall() 
	cursor.close()
	
	if (data): # has data
		return render_template('publicHome.html', statuses=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('publicHome.html', error2=error)


#####################################################################
#                              CUSTOMER                             #
#               all operations from the customer side               #
#####################################################################
# Define route for login
@app.route('/cuslogin')
def cuslogin():
	return render_template('cuslogin.html')

# Define route for register
@app.route('/cusregister')
def cusregister():
	return render_template('cusregister.html')

# Authenticates the login
@app.route('/cusloginAuth', methods=['GET', 'POST'])
def cusloginAuth():
	email = request.form['email']
	db_email = check_apostrophe(email)
	password = request.form['password']

	cursor = conn.cursor()
	query = "SELECT * FROM customer WHERE email = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(db_email, password))
	data = cursor.fetchone()
	cursor.close()
	if(data):
		session['email'] = email
		cursor = conn.cursor()
		query = "SELECT ticket_id, airline_name, airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
			FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
				 WHERE customer_email = \'{}\' and status = 'upcoming' and \
				D.airport_name = departure_airport and A.airport_name = arrival_airport"
		cursor.execute(query.format(db_email))
		data1 = cursor.fetchall() 
		cursor.close()
		return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data1)
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('cuslogin.html', error=error)

# Authenticates the register
@app.route('/cusregisterAuth', methods=['GET', 'POST'])
def cusregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	db_email = check_apostrophe(email)
	name = request.form['name']
	db_name = check_apostrophe(name)
	password = request.form['password']
	building_number = check_apostrophe(request.form['building_number'])
	street = check_apostrophe(request.form['street'])
	city = check_apostrophe(request.form['city'])
	state = check_apostrophe(request.form['state'])
	phone_number = request.form['phone_number']
	passport_number = check_apostrophe(request.form['passport_number'])
	passport_expiration = request.form['passport_expiration']
	passport_country = check_apostrophe(request.form['passport_country'])
	date_of_birth = request.form['date_of_birth']

	cursor = conn.cursor()
	query = "SELECT * FROM customer WHERE email = \'{}\'"
	cursor.execute(query.format(db_email))
	data = cursor.fetchone()
	if(data):
		cursor.close()
		error = "This user already exists"
		return render_template('cusregister.html', error = error)
	else:
		ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(db_email, db_name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		query = "SELECT ticket_id, airline_name, airplane_id, flight_num, \
			D.airport_city, \
			departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
				FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
					WHERE customer_email = \'{}\' and status = 'upcoming' and \
					D.airport_name = departure_airport and A.airport_name = arrival_airport"
		cursor.execute(query.format(db_email))
		data1 = cursor.fetchall() 
		cursor.close()
		flash("You are logged in")
		session['email'] = email
		return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data1)

@app.route('/cushome')
def cushome():
	email = session['email']
	db_email = check_apostrophe(email)

	cursor = conn.cursor()
	query = "SELECT ticket_id, airline_name, airplane_id, flight_num, \
		D.airport_city, \
		departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
			FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
				 WHERE customer_email = \'{}\' and status = 'upcoming' and \
				D.airport_name = departure_airport and A.airport_name = arrival_airport"
	cursor.execute(query.format(db_email))
	data1 = cursor.fetchall() 
	cursor.close()
	return render_template('cushome.html', email=email, emailName=email.split('@')[0], view_my_flights=data1)

@app.route('/cusSearchPurchase')
def cusSearchPurchase():
	email = session['email'] 
	return render_template('cusSearchPurchase.html', email=email, emailName=email.split('@')[0])

@app.route('/cusSpending', methods=['POST', 'GET'])
def cusSpending():
	email = session['email']
	db_email = check_apostrophe(email)

	# show total spending in the past period of time
	duration = request.form.get("duration")
	if duration is None:
		duration = "365"
	cursor = conn.cursor()
	query = 'select sum(price)\
				from customer_spending \
				where customer_email = \'{}\' and (purchase_date between DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())'
	cursor.execute(query.format(db_email, duration))
	total_spending_data = cursor.fetchone()
	cursor.close()

	# show month-wise spending in the past 6 months
	period = request.form.get("period")
	if period is None:
		period = '6'
	today = datetime.date.today()
	past_day = today.day
	past_month = (today.month - int(period)) % 12
	if past_month == 0:
		past_month = 12
	past_year = today.year + ((today.month - int(period) - 1) // 12)
	past_date = datetime.date(past_year, past_month, past_day) # the day 6 months ago

	cursor = conn.cursor()
	query2 = "select year(purchase_date) as year, month(purchase_date) as month, sum(price) as monthly_spending \
				from customer_spending \
				where customer_email = \'{}\' and purchase_date >= \'{}\' \
				group by year(purchase_date), month(purchase_date)"
	cursor.execute(query2.format(db_email, past_date))
	monthly_spending_data = cursor.fetchall()
	cursor.close()

	months = []
	monthly_spendings = []
	for i in range(int(period)):
		month = (past_date.month + i + 1) % 12
		if month == 0:
			month = 12
		year = past_date.year + ((past_date.month + i) // 12)
		flag = False
		for one_month in monthly_spending_data:
			if one_month[0] == year and one_month[1] == month:
				flag = True
				break
		if flag:
			monthly_spendings.append(int(one_month[2]))
		else:
			monthly_spendings.append(0)
		months.append(str(year)+'-'+str(month))

	return render_template('cusSpending.html', email=email, emailName=email.split('@')[0], total_spending_data=total_spending_data[0], duration=duration, period=period, months=months, monthly_spendings=monthly_spendings)

@app.route('/cusSearchFlight', methods=['GET', 'POST'])
def cusSearchFlight():
	email = session['email']
	db_email = check_apostrophe(email)
	departure_city = check_apostrophe(request.form['departure_city'])
	departure_airport = check_apostrophe(request.form['departure_airport'])
	arrival_city = check_apostrophe(request.form['arrival_city'])
	arrival_airport = check_apostrophe(request.form['arrival_airport'])
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	cursor = conn.cursor()
	query1 = "SELECT airline_name, airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, price, status, num_tickets_left\
			FROM airport as D, flight, airport AS A \
			WHERE D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\') and \
					D.airport_name = departure_airport and \
					departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
					A.airport_city = if (\'{}\' = '', A.airport_city, \'{}\')and \
					A.airport_name = arrival_airport and \
					arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\')and \
					date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\')and \
					date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\')"
	cursor.execute(query1.format(departure_city,departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date,arrival_date))
	data = cursor.fetchall()
	cursor.close()
	
	if (data):
		return render_template('cusSearchPurchase.html', email = email, emailName=email.split('@')[0], upcoming_flights=data)
	else:
		error = 'Sorry ... Flight does not exist!'
		return render_template('cusSearchPurchase.html', email = email, emailName=email.split('@')[0], error1=error)

@app.route('/cusBuyTickets', methods=['GET', 'POST'])
def cusBuyTickets():
	email = session['email']
	db_email = check_apostrophe(email)
	flight_num = request.form['flight_num']

	cursor = conn.cursor()
	# this query is an extra failsafe in case triggers went wrong.
	query = "SELECT ticket_id FROM flight NATURAL JOIN ticket\
			WHERE flight_num = \'{}\' AND \
				ticket_id NOT IN (SELECT ticket_id \
									FROM flight NATURAL JOIN ticket NATURAL JOIN purchases)\
				AND flight_num = \'{}\'"
	cursor.execute(query.format(flight_num, flight_num))
	data = cursor.fetchall()
	cursor.close()

	if(data):
		cursor = conn.cursor()
		ticket = int(data[0][0])
		ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', NULL, CURDATE())"
		cursor.execute(ins.format(ticket, db_email))
		conn.commit()
		cursor.close()
		message1 = 'Ticket bought successfully!'
		return render_template('cusSearchPurchase.html', email = email, message1 = message1)
	else:
		#returns an error message to the html page
		error = 'No ticket'
		return render_template('cusSearchPurchase.html', error2=error, email = email, emailName=email.split('@')[0])	


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
	email = request.form['email']
	db_email = check_apostrophe(email)
	password = request.form['password']

	cursor = conn.cursor()
	query = "SELECT * FROM booking_agent WHERE email = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(db_email, password))
	data = cursor.fetchone()
	cursor.close()
	if(data):
		cursor = conn.cursor()
		query1 = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
		cursor.execute(query1.format(db_email))
		data1 = cursor.fetchone()
		query2 = "SELECT * FROM agent_view_flight WHERE email = \'{}\'"
		cursor.execute(query2.format(db_email))
		data2 = cursor.fetchall()
		cursor.close()
		session['email'] = email
		return render_template('agenthome.html', email=email, emailName=email.split('@')[0], view_my_flights=data2, booking_agent_id=data1)
	else:
		error = 'Invalid login or email'
		return render_template('agentlogin.html', error=error)

@app.route('/agentregisterAuth', methods=['GET', 'POST'])
def agentregisterAuth():
	email = request.form['email']
	db_email = check_apostrophe(email)
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	cursor = conn.cursor()
	query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
	cursor.execute(query.format(db_email))
	data = cursor.fetchone()
	if(data):
		cursor.close()
		error = "This user already exists"
		return render_template('agentregister.html', error = error)
	else:
		ins = "INSERT INTO booking_agent VALUES(\'{}\', md5(\'{}\'), \'{}\')"
		cursor.execute(ins.format(db_email, password, booking_agent_id))
		conn.commit()
		query1 = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
		cursor.execute(query1.format(db_email))
		data1 = cursor.fetchone()
		# get view_my_flights info from db
		query = "SELECT * FROM agent_view_flight WHERE email = \'{}\'"
		cursor.execute(query.format(db_email))
		data2 = cursor.fetchall()
		cursor.close()
		session['email'] = email
		flash("You are logged in")
		return render_template('agenthome.html', email=email, emailName=email.split('@')[0], view_my_flights=data2, booking_agent_id=data1)

@app.route('/agentHome')
def agentHome():
	email = session['email']
	db_email = check_apostrophe(email)
		
	cursor = conn.cursor()
	query1 = "SELECT booking_agent_id FROM booking_agent WHERE email = \'{}\'"
	cursor.execute(query1.format(db_email))
	data1 = cursor.fetchone()
	query2 = "SELECT * FROM agent_view_flight WHERE email = \'{}\'"
	cursor.execute(query2.format(db_email))
	data2 = cursor.fetchall()
	cursor.close()
	return render_template('agenthome.html', email=email, emailName=email.split('@')[0], view_my_flights=data2, booking_agent_id=data1)

@app.route('/agentSearchPurchase')
def agentSearchPurchase():
	email = session['email'] 
	return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], )

@app.route('/agentCommission', methods=['POST', 'GET'])
def agentCommission():
	email = session['email']
	db_email = check_apostrophe(email)

	cursor = conn.cursor()
	duration = request.form.get("duration")
	if duration is None:
		duration = "30"
	query = 'select sum(ticket_price * 0.1), avg(ticket_price * 0.1), count(ticket_price * 0.1) from agent_commission where email = \'{}\' and (purchase_date between DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())'
	cursor.execute(query.format(db_email, duration))
	commission_data = cursor.fetchone()
	total_com, avg_com, count_ticket = commission_data
	cursor.close()
	return render_template('agentCommission.html', email=email, emailName=email.split('@')[0], total_com=total_com, avg_com=avg_com, count_ticket=count_ticket, duration=duration)

@app.route('/agentTopCustomers')
def agentTopCustomers():
	email = session['email']
	db_email = check_apostrophe(email)

	cursor = conn.cursor()
	query = "select customer_email, count(ticket_id) from agent_commission where email = \'{}\' and datediff(CURDATE(), DATE(purchase_date)) < 183 group by customer_email order by count(ticket_id) desc"
	cursor.execute(query.format(db_email))
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
	cursor.execute(query2.format(db_email))
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
	return render_template('agentTopCustomers.html', email=email, emailName=email.split('@')[0], ppl1=ppl1, ppl2=ppl2, tickets=tickets, commissions=commissions)

@app.route('/agentSearchFlight', methods=['GET', 'POST'])
def agentSearchFlight():
	email = session['email']
	db_email = check_apostrophe(email)
	departure_city = check_apostrophe(request.form['departure_city'])
	departure_airport = check_apostrophe(request.form['departure_airport'])
	arrival_city = check_apostrophe(request.form['arrival_city'])
	arrival_airport = check_apostrophe(request.form['arrival_airport'])
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	# validate booking agent email
	cursor = conn.cursor()
	query = " select booking_agent_id from booking_agent where email = \'{}\'"
	cursor.execute(query.format(db_email))
	agent_data = cursor.fetchone() # tuple (98765,)
	booking_agent_id = agent_data[0]
	cursor.close()

	if not (agent_data):
		agent_id_error = 'You are not a booking agent'
		return render_template('agentSearchPurchase.html', error1=agent_id_error)

	# booking agent email has been validated
	cursor = conn.cursor()
	query = "SELECT airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status, price, airline_name, num_tickets_left \
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
		return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('agentSearchPurchase.html', email=email, emailName=email.split('@')[0], error1=error)

@app.route('/agentBuyTickets', methods=['GET', 'POST'])
def agentBuyTickets():
	email = session['email']
	db_email = check_apostrophe(email)
	flight_num = request.form.get("flight_num")
	customer_email = check_apostrophe(request.form['customer_email'])

	# validate booking agent email
	cursor = conn.cursor()
	query = " select booking_agent_id from booking_agent where email = \'{}\'"
	cursor.execute(query.format(db_email))
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
		return render_template('agentSearchPurchase.html', error2=ticket_error, email=email, emailName=email.split('@')[0])
	else:
		cursor = conn.cursor()
		ticket_id = int(ticket_data[0][0])
		ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', \'{}\', CURDATE())"
		cursor.execute(ins.format(ticket_id, customer_email, booking_agent_id))
		conn.commit()
		cursor.close()
		message = 'Ticket bought successfully!'
		return render_template('agentSearchPurchase.html', message=message, email=email, emailName=email.split('@')[0])


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
	username = request.form['username']
	db_username = check_apostrophe(username)
	password = request.form['password']

	cursor = conn.cursor()
	query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = md5(\'{}\')"
	cursor.execute(query.format(db_username, password))
	data = cursor.fetchone()

	query1 = "SELECT username, airline_name, airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time FROM flight NATURAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(CURDATE(), DATE(departure_time)) < 30 "
	cursor.execute(query1.format(db_username))
	data1 = cursor.fetchall()
	cursor.close()
	if(data):
		session['username'] = username
		return render_template('staffhome.html', username=username, posts = data1)
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('stafflogin.html', error=error)

#Authenticates the register
@app.route('/staffregisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
	#grabs information from the forms
	username = request.form['username']
	db_username = check_apostrophe(username)
	password = request.form['password']
	first_name = request.form['first_name']
	db_first_name = check_apostrophe(first_name)
	last_name = request.form['last_name']
	db_last_name = check_apostrophe(last_name)
	date_of_birth = request.form['date_of_birth']
	airline_name = check_apostrophe(request.form['airline_name'])

	cursor = conn.cursor()
	query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
	cursor.execute(query.format(db_username))
	data = cursor.fetchone()
	if(data):
		error = "This user already exists"
		return render_template('staffregister.html', error = error)
	
	query = "SELECT airline_name FROM airline WHERE airline_name = \'{}\'"
	cursor.execute(query.format(airline_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	
	if(data):
		ins = "INSERT INTO airline_staff VALUES(\'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(db_username, password, db_first_name, db_last_name, date_of_birth, airline_name))
		conn.commit()

		query1 = "SELECT username, airline_name, airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time FROM flight NATURAL JOIN airline_staff WHERE username = \'{}\' and status = 'upcoming' and datediff(DATE(departure_time), CURDATE()) < 30 "
		cursor.execute(query1.format(db_username))
		data1 = cursor.fetchall()

		cursor.close()
		flash("You are logged in")
		session['username'] = username
		return render_template('staffhome.html', username=username, posts = data1)
	else:
		#If the previous query returns data, then user exists
		error = "This airline doesn't exist"
		cursor.close()
		return render_template('staffregister.html', error = error)

@app.route('/staffhome')
def staffhome():
	username = session['username']
	db_username = check_apostrophe(username)

	cursor = conn.cursor();
	query = "SELECT username, airline_name, airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time \
			FROM flight NATURAL JOIN airline_staff \
			WHERE username = \'{}\' and status = 'upcoming' and datediff(CURDATE(), DATE(departure_time)) < 30 "
	cursor.execute(query.format(db_username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('staffhome.html', username=username, posts=data1)

@app.route('/staffSearchFlight', methods=['GET', 'POST'])
def staffSearchFlight():
	departure_city = check_apostrophe(request.form['departure_city'])
	departure_airport = check_apostrophe(request.form['departure_airport'])
	arrival_city = check_apostrophe(request.form['arrival_city'])
	arrival_airport = check_apostrophe(request.form['arrival_airport'])
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	username = session['username']
	db_username = check_apostrophe(username)

	cursor = conn.cursor()
	query = "SELECT airline_name, airplane_id, flight_num, D.airport_city, departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status, price\
			FROM airport as D, flight NATURAL JOIN airline_staff, airport AS A \
			WHERE D.airport_city = if (\'{}\' = '',D.airport_city, \'{}\') and \
					D.airport_name = departure_airport and \
					departure_airport = if (\'{}\' = '', departure_airport, \'{}\') and \
					A.airport_city = if (\'{}\' = '', A.airport_city, \'{}\')and \
					A.airport_name = arrival_airport and \
					arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\')and \
					date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\')and \
					date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\') and \
					username = \'{}\'"
	cursor.execute(query.format(departure_city, departure_city,departure_airport,departure_airport, arrival_city, arrival_city, arrival_airport, arrival_airport, departure_date, departure_date, arrival_date,arrival_date,db_username))
	data = cursor.fetchall()
	cursor.close()
	
	if (data): # has data
		return render_template('staffflight.html', username=username, upcoming_flights=data)
	else: # does not have data
		error = 'Sorry ... Cannot find this flight!'
		return render_template('staffflight.html', username=username, error1=error)

@app.route('/staffflight')
def staffflight():
	username = session['username'] 
	return render_template('staffflight.html', username=username)

@app.route('/staffaddinfo')
def staffaddinfo():
	username = session['username'] 
	db_username = check_apostrophe(username)
	
	cursor = conn.cursor();
	query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
	cursor.execute(query.format(db_username))
	data1 = cursor.fetchall()
	cursor.close()

	return render_template('staffaddinfo.html', username=username, airplane = data1)

@app.route('/edit_status', methods=['GET', 'POST'])
def edit_status():
	status = request.form['edit_status']
	flight_num = request.form['flight_num']
	
	cursor = conn.cursor()
	upd = "UPDATE flight set status = \'{}\' WHERE flight_num = \'{}\'"
	cursor.execute(upd.format(status, flight_num))
	conn.commit()
	cursor.close()
	message = 'Status changed successfully!'
	return render_template('staffflight.html', message = message)

@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
	username = session['username']
	db_username = check_apostrophe(username)
	airline_name = check_apostrophe(request.form['airline_name'])
	flight_num = request.form['flight_num']
	departure_airport = check_apostrophe(request.form['departure_airport'])
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	arrival_airport = check_apostrophe(request.form['arrival_airport'])
	arrival_date = request.form['arrival_date']
	arrival_time = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	cursor = conn.cursor()
	query = "SELECT username, airline_name \
			FROM airline_staff \
			WHERE username = \'{}\' and airline_name = \'{}\'"
	cursor.execute(query.format(db_username, airline_name))
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	error1 = None
	if not (data):
		#If the previous query returns data, then user exists
		error1 = "Wrong airline"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(db_username))
		data1 = cursor.fetchall()
		return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1)

	query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
	cursor.execute(query.format(departure_airport))
	#stores the results in a variable
	data = cursor.fetchall()
	error1 = None
	if not (data):
		#If the previous query returns data, then user exists
		error1 = "Departure airport doesn't exist"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1)

	query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
	cursor.execute(query.format(arrival_airport))
	#stores the results in a variable
	data = cursor.fetchall()
	error1 = None
	if not (data):
		#If the previous query returns data, then user exists
		error1 = "Arrival airport doesn't exist"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1)

	query = "SELECT airplane_id FROM airplane WHERE airplane_id = \'{}\'"
	cursor.execute(query.format(airplane_id))
	#stores the results in a variable
	data = cursor.fetchall()
	error1 = None
	if not (data):
		#If the previous query returns data, then user exists
		error1 = "Airplane doesn't exist"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1)
	# cursor.close()
	#executes query
	# cursor = conn.cursor()
	query = "SELECT airline_name, flight_num FROM flight WHERE airline_name = \'{}\' and flight_num = \'{}\'"
	cursor.execute(query.format(airline_name, flight_num))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error1 = None
	
	if(data):
		#If the previous query returns data, then user exists
		error1 = "This flight already exists"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('staffaddinfo.html', error1 = error1, username=username, airplane = data1)		

	else:
		ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{},{}\', \'{}\', \'{}, {}\', \'{}\', \'{}\', \'{}\', 0)"
		cursor.execute(ins.format(airline_name, flight_num, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, price, status, airplane_id))
		conn.commit()
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		cursor.close()
		message1 = "New flight added"
		# flash()
		return render_template('staffaddinfo.html', message1 = message1, username=username, airplane = data1)

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	username = session['username']
	db_username = check_apostrophe(username)
	
	#grabs information from the forms
	airline_name = check_apostrophe(request.form['airline_name'])
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT username, airline_name FROM airline_staff WHERE username = \'{}\' and airline_name = \'{}\'"
	cursor.execute(query.format(db_username, airline_name))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error2 = None	

	if not (data):
		#If the previous query returns data, then user exists
		error2 = "Wrong airline"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(db_username))
		data1 = cursor.fetchall()
		return render_template('staffaddinfo.html', error2 = error2, username=username, airplane = data1)

	#executes query

	query = "SELECT airline_name, airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
	cursor.execute(query.format(airline_name, airplane_id))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error2 = None
	if(data):
		#If the previous query returns data, then user exists
		error2 = "This airplane already exists"
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('staffaddinfo.html', error2 = error2, username=username, airplane = data1)
	else:		
		ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
		cursor.execute(ins.format(airline_name, airplane_id, seats))

		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()

		conn.commit()
		cursor.close()
		message2 = "New airplane added"
		# flash()
		return render_template('staffaddinfo.html', message2 = message2, username=username, airplane = data1)

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	username = session['username']
	db_username = check_apostrophe(username)
	airport_name = check_apostrophe(request.form['airport_name'])
	airport_city = check_apostrophe(request.form['airport_city'])

	cursor = conn.cursor()
	airport = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
	cursor.execute(airport.format(airport_name))
	airportdata = cursor.fetchone()
	query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airline_staff WHERE username = \'{}\'"
	cursor.execute(query.format(db_username))
	data1 = cursor.fetchall()
	cursor.close()
	error3 = None
	if(airportdata):
		error3 = "This airport already exists"
		return render_template('staffaddinfo.html', error3 = error3, username=username, airplane = data1)

	else:
		cursor = conn.cursor()
		ins = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
		cursor.execute(ins.format(airport_name, airport_city))
		conn.commit()
		cursor.close()
		message3 = "New airport added"
		return render_template('staffaddinfo.html', message3 = message3, username=username, airplane = data1)

@app.route('/staffagent')
def staffagent():
	username = session['username']
	db_username = check_apostrophe(username)
	# airline_name = session['airline_name']
	cursor = conn.cursor();
	query1 = "SELECT email, booking_agent_id, sum(price) * 0.1 as commission FROM booking_agent NATURAL JOIN purchases \
		NATURAL JOIN flight NATURAL JOIN ticket AS T, airline_staff \
		WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and YEAR(purchase_date) =  YEAR(CURDATE()) - 1  \
			GROUP BY email, booking_agent_id \
				ORDER BY commission DESC\
					LIMIT 5 "
	cursor.execute(query1.format(db_username))
	data1 = cursor.fetchall()

	cursor = conn.cursor();
	query2 = "SELECT booking_agent.email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchases \
		NATURAL JOIN ticket AS T, airline_staff \
		WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and MONTH(purchase_date) =  MONTH(CURDATE()) - 1 \
			GROUP BY email, booking_agent_id \
				ORDER BY ticket DESC LIMIT 5 "
	cursor.execute(query2.format(db_username))
	data2 = cursor.fetchall()

	cursor = conn.cursor();
	query3 = "SELECT email, booking_agent_id, count(ticket_id) as ticket FROM booking_agent NATURAL JOIN purchases \
		NATURAL JOIN ticket AS T, airline_staff \
		WHERE username = \'{}\' and airline_staff.airline_name = T.airline_name and YEAR(purchase_date) =  YEAR(CURDATE()) - 1 \
			GROUP BY email, booking_agent_id \
				ORDER BY ticket DESC LIMIT 5 "
	cursor.execute(query3.format(db_username))
	data3 = cursor.fetchall()

	cursor = conn.cursor();
	query = "SELECT email, booking_agent_id FROM booking_agent"
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	return render_template('staffagent.html', username=username, commission = data1, month = data2, year = data3, posts = data)

@app.route('/staffcus')
def staffcus():
	username = session['username']
	db_username = check_apostrophe(username)
	# airline_name = session['airline_name']
	cursor = conn.cursor();
	query1 = "SELECT email, name, count(ticket_id) as ticket FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY ticket DESC LIMIT 1"
	cursor.execute(query1.format(db_username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('staffcus.html', frequent = data1, username = username)

@app.route('/staffcusflight', methods=['GET', 'POST'])
def staffcusflight():
	username = session['username']
	db_username = check_apostrophe(username)
	email = request.form['customer_email']
	db_email = check_apostrophe(email)

	cursor = conn.cursor()
	query2 = "SELECT DISTINCT airplane_id, flight_num, \
		departure_airport, arrival_airport, departure_time, arrival_time, \
			status FROM customer, \
				purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE email = \'{}\' and email = customer_email and username = \'{}\'"
	cursor.execute(query2.format(db_email, db_username))
	# cursor.execute(query2)
	data2 = cursor.fetchall()

	query1 = "SELECT email, name, count(ticket_id) as ticket FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY ticket DESC LIMIT 1"
	cursor.execute(query1.format(db_username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()

	cursor.close()
	error = None
	if(data2):
		return render_template('staffcus.html', cusflight = data2, frequent = data1, username = username)
	else:
		cursor = conn.cursor();
		cus = "SELECT email FROM customer WHERE email = \'{}\'"
		cursor.execute(cus.format(db_email))
		# cursor.execute(query2)
		cus = cursor.fetchone()
		cursor.close()
		if(cus):
			error = "Customer did not take any flight"
		# cursor.close()
		else:
			error = "No Such Customer"
		return render_template('staffcus.html', error = error, frequent = data1, username = username)

@app.route('/staffflightcus', methods=['GET', 'POST'])
def staffflightcus():
	username = session['username']
	db_username = check_apostrophe(username)
	flight_num = request.form['flight_num']

	cursor = conn.cursor();
	query3 = "SELECT DISTINCT email, name FROM customer, \
				purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
		WHERE flight_num = \'{}\' and email = customer_email and username = \'{}\'"
	cursor.execute(query3.format(flight_num, db_username))
	# cursor.execute(query2)
	data3 = cursor.fetchall()

	query1 = "SELECT email, name, count(ticket_id) as ticket FROM customer, purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff \
		WHERE email = customer_email AND username = \'{}\'\
		GROUP BY email, name\
		ORDER BY ticket DESC LIMIT 1"
	cursor.execute(query1.format(db_username))
	# cursor.execute(query1)
	data1 = cursor.fetchall()

	cursor.close()
	error3 = None
	if(data3):
		return render_template('staffcus.html', flightcus = data3, frequent = data1, username = username)
	else:
		cursor = conn.cursor();
		cus = "SELECT flight_num FROM flight NATURAL JOIN airline_staff WHERE flight_num = \'{}\'\
			AND username = \'{}\'"
		cursor.execute(cus.format(flight_num, db_username))
		# cursor.execute(query2)
		cus = cursor.fetchone()
		cursor.close()
		if(cus):
			error3 = "Flight Has No Customer"
		else:
			error3 = 'No such Flight'
		# cursor.close()
		return render_template('staffcus.html', error3 = error3, frequent = data1, username = username)
	
@app.route('/staffDestReve')
def staffDestReve():
	username = session['username']
	db_username = check_apostrophe(username)

	cursor = conn.cursor();
	query1 = "SELECT airport_city, count(ticket_id) AS ticket FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and MONTH(purchase_date) >  MONTH(CURDATE()) - 3\
		GROUP BY airport_city\
		ORDER BY ticket DESC\
			 LIMIT 3"
	cursor.execute(query1)
	month = cursor.fetchall()

	query2 = "SELECT airport_city, count(ticket_id) AS ticket FROM \
		purchases NATURAL JOIN ticket NATURAL JOIN flight, airport \
		WHERE airport_name = arrival_airport and YEAR(purchase_date) =  YEAR(CURDATE()) - 1\
			GROUP BY airport_city\
		ORDER BY ticket DESC\
			LIMIT 3"
	cursor.execute(query2)
	# cursor.execute(query1)
	year = cursor.fetchall()

	query3 = "SELECT sum(price)\
	FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
	WHERE username = \'{}\' AND booking_agent_id is NULL AND MONTH(purchase_date) =  MONTH(CURDATE()) - 1\
	GROUP BY airline_name"

	cursor.execute(query3.format(db_username))
	# cursor.execute(query1)
	mdirect = cursor.fetchall()
	if(mdirect):
		mdirect = [json.dumps(mdirect[0][0],cls=DecimalEncoder)]
	else:
		mdirect = [0]

	query4 = "SELECT sum(price)\
	FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
	WHERE username = \'{}\' AND booking_agent_id is NOT NULL AND MONTH(purchase_date) =  MONTH(CURDATE()) - 1\
	GROUP BY airline_name"
	
	cursor.execute(query4.format(db_username))
	# cursor.execute(query1)
	mindirect = cursor.fetchall()
	if(mindirect):
		mindirect = [json.dumps(mindirect[0][0],cls=DecimalEncoder)]
	else:
		mindirect = [0]

	query5 = "SELECT sum(price)\
	FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
	WHERE username = \'{}\' AND booking_agent_id is NULL AND YEAR(purchase_date) =  YEAR(CURDATE()) - 1\
	GROUP BY airline_name"
	
	cursor.execute(query5.format(db_username))
	# cursor.execute(query1)
	ydirect = cursor.fetchall()
	if(ydirect):
		ydirect = [json.dumps(ydirect[0][0],cls=DecimalEncoder)]
	else:
		ydirect = [0]

	query6 = "SELECT sum(price)\
	FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff\
	WHERE username = \'{}\' AND booking_agent_id is NOT NULL AND YEAR(purchase_date) =  YEAR(CURDATE()) - 1\
	GROUP BY airline_name"
	
	cursor.execute(query6.format(db_username))
	# cursor.execute(query1)
	yindirect = cursor.fetchall()
	if(yindirect):
		yindirect = [json.dumps(yindirect[0][0],cls=DecimalEncoder)]
	else:
		yindirect = [0]
	
	cursor.close()
	return render_template('staffDestReve.html', month = month, year = year, username = username, mdirect = mdirect, mindirect = mindirect, ydirect = ydirect, yindirect = yindirect)

@app.route('/staffTickets')
def staffTickets():
	username = session['username']
	return render_template('staffTickets.html', username = username)

@app.route('/staffticket', methods=['GET', 'POST'])
def staffticket():
	username = session['username']
	db_username = check_apostrophe(username)
	start = request.form['start']
	duration = request.form.get("duration")
	end = request.form['end']

	cursor = conn.cursor()
	if duration == "":
		ticket = "SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, count(ticket_id) FROM \
				purchases NATURAL JOIN airline_staff NATURAL JOIN flight NATURAL JOIN ticket\
				WHERE purchase_date > \'{}\'\
				and purchase_date < \'{}\' AND username = \'{}\' \
				GROUP BY year, month, airline_name"
		cursor.execute(ticket.format(start, end, db_username))
		# cursor.execute(query2)
		allticket = cursor.fetchall()
	elif duration == 'tmonth':
		ticket = "SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, count(ticket_id) FROM \
				purchases NATURAL JOIN airline_staff NATURAL JOIN flight NATURAL JOIN ticket\
				WHERE MONTH(purchase_date) =  MONTH(CURDATE()) - 1 AND username = \'{}\' \
				GROUP BY year, month, airline_name"

		cursor.execute(ticket.format(db_username))
		# cursor.execute(query1)
		allticket = cursor.fetchall()
	elif duration == 'tyear':
		ticket = "SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, count(ticket_id) FROM \
				purchases NATURAL JOIN airline_staff NATURAL JOIN flight NATURAL JOIN ticket\
				WHERE YEAR(purchase_date) =  YEAR(CURDATE()) - 1 AND username = \'{}\' \
				GROUP BY year, month, airline_name"

		cursor.execute(ticket.format(db_username))
		# cursor.execute(query1)
		allticket = cursor.fetchall()

	cursor.close()


	if(allticket):
		time = [str(allticket[i][0]) + '-' + str(allticket[i][1]) for i in range(len(allticket))]
		monthticket = [allticket[i][2] for i in range(len(allticket))]

		# time = ['2020-10', '2020-11']
		# monthticket = [1, 2]
		return render_template('staffTickets.html', time = time, monthticket = monthticket, ticket = allticket, username = username)
	else:
		error = "No ticket sold"
		# cursor.close()
		return render_template('staffTickets.html', error = error, username = username)


#####################################################################
#                             COMMON                                #
#                   all operations from all sides                   #
#####################################################################
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/stafflogin')

@app.route('/logoutEmail')
def logoutEmail():
	session.pop('email')
	return redirect('/cuslogin')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
