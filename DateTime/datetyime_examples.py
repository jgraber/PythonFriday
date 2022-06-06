from datetime import datetime, timedelta

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

print("-" * 50)

tomorrow = today + timedelta(days=1)
print(tomorrow)

print("-" * 50)

print(f"Date part only: {tomorrow.date()}")