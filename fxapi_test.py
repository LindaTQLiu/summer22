from flask import request, Flask
from datetime import datetime as dt
sp = dt.strptime
import pandas as pd
import json

df = pd.read_pickle("currency_codes.pkl")        # load the list of all ISO currency codes.

'''
def date(input_date):
    return sp(input_date, "%Y-%m-%d")            # define the date format accepted in requests.   # replaced with manual formatting.
'''

app = Flask(__name__)
@app.route('/request', methods=['GET'])          # expected request: [ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]
def process_data():
    currencies = request.args.get("currencies")
    in_date = request.args.get("date")

    # Validate date input.
    raw_date = in_date.split("-")
    date_errormsg = {
        "error message: ": "Please enter a valid date in the format of year-month-day; eg. 2001-6-19, 2020-03-2", 
        "expected request format": "[ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]"}
    if len(raw_date)!=3: return json.dumps(date_errormsg)
    for i in range(3):
        if not raw_date[i].isdigit(): return json.dumps(date_errormsg)
        raw_date[i] = int(raw_date[i])
    in_date = dt(raw_date[0], raw_date[1], raw_date[2], 7, 0, 0, 1, )                       # check whether the input date is in the correct format. If yes, change to datetime type.


    # Validate currencies input. 
    raw_cur = currencies.split("-")
    if len(raw_cur)==2:
        cur1, cur2 = raw_cur[0].upper(), raw_cur[1].upper()
        if not(cur1 in df and cur2 in df):
            code_err = {
                "error message": "Please enter two ISO currency codes for currencies.; eg. gbp-usd (case-insensitive)", 
                "expected request format": "[ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]"}
            return json.dumps(code_err)
    else: 
        return json.dumps(code_err)
    
    from forex_python.converter import CurrencyRates as cr
    c = cr()                                      # source of fx rates.
    output = c.get_rate(cur1, cur2, in_date)
    return json.dumps(output)
    
app.run(host='0.0.0.0', debug=True)


'''
# construct a json object, return whatever values i think are necessary;
# 214 error response, http header saying error or whatever
current schema, singular scheme for all failures
for ease of troubleshoot
return object as json, write another py script to do pytest
'''

