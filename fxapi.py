from flask import request, Flask
from datetime import datetime as dt
sp = dt.strptime
import pandas as pd

df = pd.read_pickle("currency_codes.pkl")

def date(input_date):
    return sp(input_date, "%Y-%m-%d")


app = Flask(__name__)
@app.route('/request', methods=['GET'])
def process_data():
    currencies = request.args.get("currencies")
    in_date = request.args.get("date")
    
    cur1, cur2 = currencies.split("-")
    cur1, cur2 = cur1.upper(), cur2.upper()
    
    assert cur1 in df and cur2 in df, "ISO currency codes only. "
    in_date = date(in_date)
    
    from forex_python.converter import CurrencyRates as cr
    c = cr()
    output = c.get_rate(cur1, cur2, in_date)
    return str(output)
    
app.run(host='0.0.0.0', debug=True)


'''
# construct a json object, return whatever values i think are necessary;
# 214 error response, http header saying error or whatever
current schema, singular scheme for all failures
for ease of troubleshoot
return object as json, write another py script to do pytest
'''

