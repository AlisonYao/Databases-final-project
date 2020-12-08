@app.route('/agentHome')
def agentHome():
	if session.get('username'):
		
	else:
		return render_template('404.html')




if "email" in request.form and 'password' in request.form:
		
	else:
		return render_template('404.html')
