from datetime import datetime, timedelta

start = datetime(2023, 10, 13, 15, 00, 00)
# print(start)


for i in range(1,100):
    start = start + timedelta(milliseconds=10)
    print(start)
    print(f"{str(start)[0:-3]}")