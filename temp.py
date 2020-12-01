import datetime
period = 24


today = datetime.date.today()
print(today)
past_day = today.day
past_month = (today.month - int(period)) % 12
if past_month == 0:
    past_month = 12
past_year = today.year + ((today.month - int(period) - 1) // 12)

print(past_year, past_month, past_day)
