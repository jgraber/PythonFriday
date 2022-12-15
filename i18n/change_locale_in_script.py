import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'de_CH')
print(f"Current locale: {locale.getlocale()}")

print(f"{datetime.today().strftime('%A')}")

locale.setlocale(locale.LC_ALL, 'en_GB')

print(f"Current locale: {locale.getlocale()}")
print(f"{datetime.today().strftime('%A')}")