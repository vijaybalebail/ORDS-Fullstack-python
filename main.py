from flask import Flask, render_template, redirect, request, session
import requests
import IdcsClient
import json
import base64
from bottle import route, run, template
import cx_Oracle
import os


app = Flask(__name__)


index_html = '''My first web app! By <strong>{{ author }}</strong>.'''


@app.route('/')
def index():
    return template(index_html, author='Real Python')


@app.route('/name/<name>')
def name(name):
    return template(index_html, author=name)



@app.route('/restapi',  methods=["POST","GET"])
def restapi():
    
    fullstack_auth_url = "https://fp7cb75hkszpygo-db202201121316.adb.us-sanjose-1.oraclecloudapps.com/ords/admin/oauth/token"



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

    #response = requests.get(url_link , headers=auth_token_header)
    # no authentication
    response = requests.get(url_link )

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
    app.run(host='0.0.0.0', debug=True, port=8080)


