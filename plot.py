import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime

hours = dates.HourLocator()
hoursFmt = dates.DateFormatter('%H:%M')

data = pandas.read_csv('OD.csv')
data2 = pandas.read_csv('Temperature.csv')

value = data.iloc[:, 1]
value2 = data2.iloc[:, 1]

time = data.iloc[:, 3]
time2 = data2.iloc[:, 3]

time_object = [0] * len(time)
time_object2 = [0] * len(time2)

for i in range(len(time)):
    time_object[i] = datetime.strptime(time[i], "%Y-%m-%d %H:%M:%S %Z")
    time_object2[i] = datetime.strptime(time2[i], "%Y-%m-%d %H:%M:%S %Z")

dates1 = dates.date2num(time_object)
dates2 = dates.date2num(time_object2)

fig, ax = plt.subplots()


ax.plot_date(dates1, value, "-", color = "#0f39f1")
plt.title("OD by time (18-19th of June)")
plt.xlabel("Time")
plt.ylabel("OD")


ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
ax.grid()

fig.autofmt_xdate()

plt.show()

fig, ax = plt.subplots()

ax.plot_date(dates2, value2, "-", color ="#b50c2b")
plt.title("Temperature by time (18th-19th of June)")
plt.xlabel("Temperature")
plt.ylabel("OD")

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
ax.grid()

fig.autofmt_xdate()

plt.show()