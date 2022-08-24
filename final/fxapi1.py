#==================================================================================#
# Author       : Linda Liu                                                         #  
# Company      : Tradeteq                                                          # 
# Script Name  : fxapi.py                                                          #
# Description  : Take a pair of currencies and a date, return fx rate or 'Nal'.    #
#==================================================================================#


from flask import request, Flask, json, send_file
from datetime import date as dt
import datetime
import pandas as pd
import requests
from functions import *

#adding common module path to sys
import sys
if '../common/' not in sys.path:
    sys.path.append('../common/')

from common.myutils import *

# set up configuration and logging
_modulename = "fxapi"
cfgname = "DEFAULT"
cfg = getconfig(_modulename, cfgname)
log = setuplog(_modulename, cfg)

LogPath = getLogPath(_modulename)
CfgPath = getCfgPath(_modulename)

time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

log.info("-------------------------------------------------------------------------------------")
log.info("                                S T A R T                   " + time_now )
log.info("-------------------------------------------------------------------------------------")
log.info("Config file:                   " + CfgPath)
log.info("Config used:                   " + cfgname)
log.info("Log file:                      " + LogPath)
log.info("File logging level:            " + cfg["filelogging"])
log.info("Console logging level:         " + cfg["consolelogging"])

log.info("-------------------------------------------------------------------------------------")


df = pd.read_pickle("currency_codes.pkl")        # load the list of all ISO currency codes.

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
# expected request: [ip address and port]/rates?currencies=[currency1]-[currency2]&date=[year]-[month]-[day]
def process_data():
    currencies = request.args.get("currencies")
    in_date = request.args.get("date")

    gurl = get_url(currencies, in_date)
    if type(gurl)==list:
        pass
    else:
        log.error(gurl)       # something wrong with the input, specified by gurl.
        response = app.response_class(
            response = json.dumps('Nal'), 
            status = 400, 
            mimetype = 'application/json'
        )
        return response

    # input for the two attributes have been validated. 
    url = gurl[0]
    response = requests.get(url)
    data = response.json()
    try: 
        data = data['rates']
    except KeyError:
        log.warning('Rates not available for the requested date.')
        response = app.response_class(
            response = json.dumps('Nal'), 
            status = 500, 
            mimetype = 'application/json'
        )
        return response


    proc_currencies = gurl[1]        # list of the two processed currencies. 
    rates = []
    for cur in proc_currencies:
        rate = get_rate(cur, data)
        if type(rate) == str:       # rate not available for this currency in the request. 
            log.warning(rate)
            response = app.response_class(
                response = json.dumps('Nal'), 
                status = 500, 
                mimetype = 'application/json'
            )
            return response
        else:
            rates.append(rate)

    output = rates[1]/rates[0]
    log.info(str(output)+' Successful request. ')
    response = app.response_class(
        response = json.dumps(output), 
        status = 200, 
        mimetype = 'application/json'
    )
    return response

@app.route('/logs', methods=['GET'])
def logs():
    return '''
        <html><body>
        Hello. <a href="/getLog">Click here to download the logs.</a>
        </body></html>
        '''

@app.route("/getLog")
def getLog():
    # from os.path import join
    return send_file(
        LogPath,
        mimetype='text/log',
        as_attachment=True
    )


app.run(debug=True)

if __name__ == '__main__': 
    # app.run(host='0.0.0.0', debug=True)
    app.run()

