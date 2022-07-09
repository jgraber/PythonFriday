from calendar import month
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

date_string = 'Jun 1 2005 1:33PM'
datetime_object = datetime.strptime(date_string, '%b %d %Y %I:%M%p')
print(datetime_object)
print(f"datetime string: {date_string}")
print(f"datetime object: {datetime_object}")
print(f"year: {datetime_object.year}")
print(f"month: {datetime_object.month}")
print(f"day: {datetime_object.day}")
print(f"hour: {datetime_object.hour}")
print(f"minute: {datetime_object.minute}")

print("-" * 50)

date_iso = "2022-06-30 20:00:00"
print(f"iso datetime string: {date_iso}")
datetime_object = datetime.fromisoformat(date_iso)
print(f"datetime object: {datetime_object}")

print("-" * 50)

today = datetime.today()
print(f"Today: {today}")
print(f"Day: {today.strftime('%A')}")
print(f"Day of week: {today.weekday()}") # Monday: 0, Sunday: 6 https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
print(f"Day of year: {today.timetuple().tm_yday}")
print(f"Week in year: {today.isocalendar()[1]}")
print(f"Week in year: {today.strftime('%V')}")
print(today.isocalendar())

print("-" * 50)

tomorrow = today + timedelta(days=1)
print(tomorrow)

print("-" * 50)

print(f"Date part only: {tomorrow.date()}")

print("-" * 50)

end_january = date.fromisoformat('2022-01-31')
result = end_january + relativedelta(months=1)
print(f"31. January + 1 months: {result}")
feb_plus_months = result + relativedelta(months=1)
print(f"28. February + months=1: {feb_plus_months}")
feb_plus_month = result + relativedelta(month=1)
print(f"28. February + month=1: {feb_plus_month}")

print("-" * 50)

christmas = datetime.fromisoformat(f"{today.year}-12-25")
diff = christmas - today
print (f"days until christmas: {diff.days}")

print("-" * 50)

christmas = datetime.fromisoformat(f"{today.year-1}-12-25")
diff = today - christmas
print (f"days since last christmas: {diff.days}")
print(result)
print(result + relativedelta(months=1))
print(result + relativedelta(month=1))

print("-" * 50)

# Date
# >>> from datetime import date
# >>> today = date.today()
# >>> today
# datetime.date(2022, 6, 14)
# >>> christmas = date(2022,12,25)
# >>> christmas
# datetime.date(2022, 12, 25)
# >>> days_to_christmas = christmas - today
# >>> days_to_christmas
# datetime.timedelta(days=194)
# >>> days_to_christmas.resolution
# datetime.timedelta(microseconds=1)
# >>> days_to_christmas.total_seconds()
# 16761600.0
# https://docs.python.org/3/library/datetime.html
# >>> new_year = date.fromisoformat("2023-01-01")
# >>> new_year
# datetime.date(2023, 1, 1)
# >>> new_year - today
# datetime.timedelta(days=201)