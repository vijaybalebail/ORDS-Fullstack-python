from flask import Flask, render_template, redirect, request, session
import requests
import IdcsClient
import json
import base64

app = Flask(__name__)

# secret key is needed for session
app.secret_key = 'secret'


@app.route("/hello")
def hello():
    #app.config.from_pyfile('config.cfg')
    return '<h1>' + 'hi sso tester' + '</h1>'


# Definition of the /auth route
@app.route('/auth', methods=['POST', 'GET'])
def auth():

    # Loading the configurations
    options = getoptions()

    # Authentication Manager loaded with the configurations
    am = IdcsClient.AuthenticationManager(options)

    '''
    Using Authentication Manager to generate the Authorization Code URL, passing the
    application's callback URL as parameter, along with code value and code parameter
    '''
    url = am.getAuthorizationCodeUrl(options["redirectURL"], options["scope"], "1234", "code")

    # Redirecting the browser to the Oracle Identity Cloud Service Authorization URL.
    return redirect(url, code=302)

# Function used to load the configurations from the config.json file
def getoptions():
    fo = open("config.json", "r")
    config = fo.read()
    options = json.loads(config)
    return options


# Definition of the /logout route
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    id_token = (session.get("id_token", None))
    if id_token is None:
       return render_template('login.html')

    options = getoptions()

    url = options["BaseUrl"]
    url += options["logoutSufix"]
    url += '?post_logout_redirect_uri=https%3A%2F%2Fdocs.oracle.com%2Fsolutions&id_token_hint='
    url += id_token
    print (url + " is the url") 

    # clears Flask client-side session (also works on refresh)
    session.clear()

    # Redirect to Oracle Identity Cloud Service logout URL
    #return redirect(url, code=302)
    return redirect(url, code=302)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def home():

    # first call IDCS API to get id_token; should return 400 status if not authenticated
    # if statement to kick you back to login if status is 400
    # if authenticated, status 200 allows app to render protected html

    options = getoptions()

    # 'code' is authorization code which is needed to get id_token
    # uses flask.request library (different from Python requests library)
    session['code'] = request.args.get('code')

    data = {
        'grant_type': 'authorization_code',
        'code': session['code'],
        'redirect_uri': options['redirectURL']
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    response = requests.post(options['BaseUrl'] + '/oauth2/v1/token?', data=data, headers=headers,
                             auth=(options['ClientId'], options['ClientSecret']))

    session['id_token'] = response.json().get("id_token")
    #print (response.json())
    print(session['id_token']) 
    print("is the id_token for SSO ")

    
 
    if str(response.status_code) != "200":
        return render_template('login.html')

    #return render_template('home.html')
    return redirect('/restapi')


@app.route('/restapi',  methods=["POST","GET"])
def restapi():
    
    id_token = (session.get("id_token", None))
    if id_token is None:
       return render_template('login.html')


    client_id = 'xtcLYtHJfz6ejruDsCcZjQ..'
    client_secret = 'yzOfoU07DQmOuYQf9jlOQg..'
    grant_type = "client_credentials"

    data = {
       "grant_type": grant_type,
       "client_id": client_id,
       "client_secret": client_secret
     }

    #data = {
    #   "grant_type": grant_type,
    #   "client_id": "xtcLYtHJfz6ejruDsCcZjQ..",
    #   "client_secret": "yzOfoU07DQmOuYQf9jlOQg.."
    # }
    fullstack_auth_url = "https://fp7cb75hkszpygo-db202201121316.adb.us-sanjose-1.oraclecloudapps.com/ords/admin/oauth/token"

    auth_response = requests.post(fullstack_auth_url, auth=(client_id,client_secret),data=data)

    auth_response_json = auth_response.json()

    auth_token = auth_response_json["access_token"]

    auth_token_header_value = "Bearer %s" % auth_token

    auth_token_header = {"Authorization": auth_token_header_value}
   # print (auth_token)
   # print (auth_response.json())
   # print( " is the auth_token_response or ords\n")


    age1 = 1
    balance = 1
    rate = 1
    age1 = request.form.get("age1")
    balance = request.form.get("balance")
    rate = request.form.get("rate")
    min = balance
    if age1 is None:
      age1 = 0
    if balance is None:
      balance = 0
    if rate is None:
      rate = '0'
    url_link = 'https://fp7cb75hkszpygo-db202201121316.adb.us-sanjose-1.oraclecloudapps.com/ords/admin/rest-rc1/rc1/'+str(age1)+'/'+str(balance)+'/'+str(rate)
    print(url_link)
    #url_link = 'https://fp7cb75hkszpygo-db202201121316.adb.us-sanjose-1.oraclecloudapps.com/ords/admin/rest-rc1/rc1/55/3000000/0.09'

    response = requests.get(url_link , headers=auth_token_header)
    jsondata = response.json()
    jsonStr = json.dumps(jsondata)
    pythonObj = json.loads(jsonStr)


    ages = []
    balances = []
    for dictionary in pythonObj['items']:
       ages.append(dictionary['age'])
       balances.append(dictionary['balance'])
       max = dictionary['balance']

    return render_template('bar_chart.html', title='Compound Interest rate of '+ rate + '%', max=max, min=min ,labels=ages, values=balances)



if __name__ == '__main__':
    #app.run(port=8080, debug=True)
    app.run(host='0.0.0.0', debug=True, port=8080)

