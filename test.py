from datetime import datetime as dt

'''
sp = dt.strptime

def date(input_date):
    return sp(input_date, "%Y-%m-%d")

date1 = date('2022-7-17')
date2 = date('2022-7-18')

print(str(date1)+'\n'+str(date2))
'''

a = dt(2022,1,2,7,0,00,1,)
print(type(a), str(a))