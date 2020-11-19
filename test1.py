#!C:/Users/lx615/AppData/Local/Programs/Python/Python38-32/python

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                       user='root',
                       password='86466491@Alison',
                       database='temp')


#Define a route to hello function
@app.route('/')
def publicHome():
	return render_template('publicHome.html')

@app.route('/publicSearchFlight', methods=['GET', 'POST'])
def publicSearchFlight():
    departure_city = request.form['departure_city']
    departure_airport = request.form['departure_airport']
    arrival_city = request.form['arrival_city']
    arrival_airport = request.form['arrival_airport']

    cursor = conn.cursor()
    query = "select * \
            from airport as D, flight, airport as A \
            where D.airport_name = flight.departure_airport and flight.arrival_airport = A.airport_name and \
            D.airport_name = \'{}\' and A.airport_name = \'{}\'"
    cursor.execute(query.format(departure_airport, arrival_airport))
    data = cursor.fetchall() 
    cursor.close()
    
    error = None
    if (data): # has data
        return render_template('publicHome.html', upcoming_flights=data)
    else: # does not have data
        error = 'Sorry ... Cannot find this flight!'
        return render_template('publicHome.html', error=error)

# @app.route('/publicSearchStatus', methods=['GET', 'POST'])
# def publicSearchFlight():
# 	pass

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


#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT email FROM customer WHERE email = \'{}\'"
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
		return render_template('testindex.html')

@app.route('/agentlogin')
def agentlogin():
	return render_template('agentlogin.html')

#Define route for register
@app.route('/agentregister')
def agentregister():
	return render_template('agentregister.html')

#Authenticates the login
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
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('agenthome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('agentlogin.html', error=error)

#Authenticates the register
@app.route('/agentregisterAuth', methods=['GET', 'POST'])
def agentregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT email FROM booking_agent WHERE email = \'{}\'"
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
		cursor.close()
		flash("You are logged in")
		return render_template('testindex.html')

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

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT username FROM airline_staff WHERE username = \'{}\'"
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
		
		flash("You are logged in")
		return render_template('staffhome.html')
	else:
		#If the previous query returns data, then user exists
		error = "This airline doesn't exist"
		cursor.close()
		return render_template('staffregister.html', error = error)
		

# @app.route('/cushome')
# def home():
    
#     email = session['email']
#     cursor = conn.cursor()
#     query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
#     cursor.execute(query.format(username))
#     data1 = cursor.fetchall() 
#     cursor.close()
#     return render_template('cushome.html', username=username, posts=data1)

		
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

@app.route('/staffhome')
def staffhome():
	username = session['username']
    # airline_name = session['airline_name']
	cursor = conn.cursor();
	query = "SELECT * FROM staff_flight ORDER BY FIELD (status, 'upcoming', 'in-progress', 'delayed')"
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('staffhome.html', username=username, posts=data1)

@app.route('/addinfo')
def addinfo():
	return render_template('addinfo.html')

@app.route('/edit_status', methods=['GET', 'POST'])
def edit_status():
	return render_template('addinfo.html')

@app.route('/creat_flight', methods=['GET', 'POST'])
def creat_flight():
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

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

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
#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

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
#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

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

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
