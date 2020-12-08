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

check_apostrophe("23456")
