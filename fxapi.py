'''
from locale import currency
from flask import request, Flask

app = Flask(__name__)

@app.route('/fxrate', methods=['GET'])
def fxrate():
    curr_1 = request.args.get('curr_1')
    curr_2 = request.args.get('curr_2')
    date = request.args.get('date')
    from hellofx import getfx
    return getfx(curr_1, curr_2, date)

app.run(host='0.0.0.0', debug= True)
'''


'''
from flask import request
@app.route('/login', methods=['GET'])
    def login():
        username = request.args.get('username')
        print(username) #This will print alex
        password= request.args.get('password')
        print(password) #This will print pw1
'''

from flask import request, Flask
from datetime import datetime as dt
sp = dt.strptime
import pandas as pd

df = pd.read_pickle("currency_codes.pkl")
#print(df)
#print(type(df), type(df[1]))


def date(input_date):
    return sp(input_date, "%Y-%m-%d")


app = Flask(__name__)
@app.route('/request', methods=['GET'])
# @app.route('/request?<currencies>&<in_date>', methods=['GET'])
def process_data():
    currencies = request.args.get("currencies")
    in_date = request.args.get("date")
    
    cur1, cur2 = currencies.split("-")
    cur1, cur2 = cur1.upper(), cur2.upper()
    # return (str(cur1)+str(cur2))
    
    assert cur1 in df and cur2 in df, "ISO currency codes only. "
    in_date = date(in_date)
    
    from forex_python.converter import CurrencyRates as cr
    c = cr()
    output = c.get_rate(cur1, cur2, in_date)
    return str(output)
    
# if __name__ == "__main__":
app.run(host='0.0.0.0', debug=True)

'''
# construct a json object, return whatever values i think are necessary;
# 214 error response, http header saying error or whatever
current schema, singular scheme for all failures
for ease of troubleshoot
return object as json, write another py script to do pytest
'''

