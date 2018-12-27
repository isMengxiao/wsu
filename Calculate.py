import datetime

months = [0, 31, 28, 31, 30,
          31, 30, 31, 31,
          30, 31, 30, 31]
print("名目利率：", end='')
mingmulilv = float(input())
print("成本利率：", end='')
chengbenlilv = float(input())
print("票面金额：", end='')
piaomianjine = float(input())
print("票面到期日期(年)：", end='')
year = int(input())
print("票面到期日期(月)：", end='')
month = int(input())
print("票面到期日期(日)：", end='')
day = int(input())
thisday = datetime.date.today()
thisyearsday = 0
for i in range(month):
    thisyearsday += months[i]
thisyearsday += day

olddays = 0
for j in range(thisday.month):
    olddays += months[i]
olddays += thisday.day
days = thisyearsday - olddays
real = (mingmulilv - chengbenlilv)/365*days*piaomianjine
print('\n\n实际利率：', real)