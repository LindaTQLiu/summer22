from flask import request, Flask
from datetime import datetime as dt
import pandas as pd

df = pd.read_pickle("currency_codes.pkl")        # load the list of all ISO currency codes.

'''
def date(input_date):
    return sp(input_date, "%Y-%m-%d")            # define the date format accepted in requests.   # replaced with manual formatting.
'''

loggings = ""

app = Flask(__name__)
@app.route('/request', methods=['GET'])          # expected request: [ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]
def process_data():
    currencies = request.args.get("currencies")
    in_date = request.args.get("date")

    requested_format = "expected request format: [ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]"

    # Validate date input.
    try:
        raw_date = in_date.split("-")
    except AttributeError:
        print("\"date\" attribute missing. "+requested_format)
        return "Nal"
    date_errormsg = {
        "error message: ": "Please enter a valid date in the format of year-month-day; eg. 2001-6-19, 2020-03-2", 
        "expected request format": "[ip address and port]/request?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]"}
    if len(raw_date)==3:
        unproc_date = [0,0,0]
        for i in range(3):
            if raw_date[i].isdigit():
                unproc_date[i] = int(raw_date[i])
            else:
                print(date_errormsg)
                return "Nal"
        try:
            proc_date = dt(unproc_date[0], unproc_date[1], unproc_date[2], 7, 0, 0, 1, )                       # check whether the input date is in the correct format. If yes, change to datetime type.
        except ValueError:
            print(date_errormsg)
            return "Nal"
    else: 
        print(date_errormsg)
        return "Nal"

    # Validate currencies input. 
    try:
        raw_cur = currencies.split("-")
    except AttributeError:
        print("\"currencies\" attribute missing. "+requested_format)
        return "Nal"
    if len(raw_cur)==2:
        cur1, cur2 = raw_cur[0].upper(), raw_cur[1].upper()
        if cur1 in df and cur2 in df:
            pass
        else: 
            return "Nal"
    else: 
        return "Nal"
    
    from forex_python.converter import CurrencyRates as cr
    c = cr()      # source of fx rates.
    try:
        output = c.get_rate(cur1, cur2, proc_date)
        return str(output)
    except ValueError:
        return "Nal"
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)



