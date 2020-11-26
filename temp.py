import datetime

today = datetime.date.today()

future_day = today.day
future_month = (today.month + 6) % 12
future_year = today.year + ((today.month + 6) // 12)

six_months_later = datetime.date(future_year, future_month, future_day)

# print(six_months_later)

for i in range(6):
	month = (today.month + i) % 12
	if month == 0:
		month = 12
	year = today.year + ((today.month + i) // 12)
	print(month, year)


