import locale
from datetime import date, timedelta
from dateutil.relativedelta import *

locale.setlocale(locale.LC_ALL, 'de_DE')

year = date(2024,1,1)

tuesday = year + relativedelta(day=2)

while tuesday.year == year.year:
    print(f'Sitzung vom {tuesday.strftime("%#d %B %Y")}')
    tuesday = tuesday + relativedelta(weeks=1)

#exit()


year = date(2024,1,1)

tuesday = year + relativedelta(day=2)
friday = year + relativedelta(day=5)
counter = 0
previous_month = ""
python_friday = 208

def print_day(day, number, previous_month, text):
    number = number + 1
    month = day.strftime("%B")

    if previous_month == month:
        print_month = ""
    else:
        print_month = month
    print(f'{print_month}, {number}, {day.strftime("%#d")}, {text}')
    day = day + relativedelta(weeks=1)
    previous_month = month
    return number, day, previous_month

while tuesday.year == year.year or friday.year == year.year:
    counter, tuesday, previous_month = print_day(tuesday, counter, previous_month, "")
    counter, friday, previous_month = print_day(friday, counter, previous_month, f"PF {python_friday}")
    python_friday = python_friday + 1



# print(tuesday)

# print(year.weekday())