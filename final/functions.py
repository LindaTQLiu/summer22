def get_url(currencies, in_date):
    # Validate date input.
    try:
        raw_date = in_date.split("-")
    except AttributeError:
        return "\"date\" attribute missing. "
        
    if len(raw_date)==3:
        temp_date = []
        for i in range(3):
            if raw_date[i].isdigit():
                temp_date.append(int(raw_date[i]))
            else:
                return "\"date\" attribute needs to be in the format of year-month-day where all three must be digits. "
        try:       # See if the input date is valid. 
            dt(temp_date[0],temp_date[1],temp_date[2])
        except ValueError:
            return "Date input can't be turned into datetime object. "
        for i in range(3):
            if len(raw_date[i]) == 1:
                raw_date[i] = '0'+raw_date[i]
        
        proc_date = '-'.join(raw_date)

    else: 
        return "\"date\" attribute needs to be in the format of year-month-day where all three must be digits. "

    # Validate currencies input. 
    try:
        raw_cur = currencies.split("-")
    except AttributeError:
        return "\"currencies\" attribute missing. "
    if len(raw_cur) == 2:
        pass
    else:
        return 'Attribute \"currencies\" requires a pair of iso currencies separated with \'-\''
    for i in range(2):
        raw_cur[i] = raw_cur[i].upper()
        if raw_cur[i] in df:
            pass
        else: 
            return '\"'+raw_cur[i]+"\" not in recognised currencies. "
    
    return ['https://api.exchangerate.host/'+proc_date, raw_cur]


def get_rate(cur, data):
    try:
        return data[cur]
    except KeyError:
        return 'Rate not available for '+cur+'. '


'''def response(msg, status):
    return app.response_class(
        response = json.dumps(msg), 
        status = status, 
        mimetype = 'application/json'
    )'''