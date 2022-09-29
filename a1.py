"""
Simple Python application to show CI/CD capabilities.
"""

import cx_Oracle
import os
from bottle import route, run, template

index_html = '''My first web app! By <strong>{{ author }}</strong>.'''


@route('/')
def index():
    return template(index_html, author='Real Python')


@route('/name/<name>')
def name(name):
    return template(index_html, author=name)

@route('/employees')
def emp():
    sql = '''select sysdate from dual '''
    employees = '''<table border=1><tr><td> date </td></tr>'''
    cursor = connection.cursor()
    for res in cursor.execute(sql):
        employees += '<tr><td>' + str(res[0]) + '</td></tr>'
    employees += '</table>'
    return str(employees)

if __name__ == '__main__':

	#un = os.environ.get('APP_USER')
	#pw = os.environ.get('APP_PASSWORD')
	#cs = os.environ.get('APP_CONNECTIONSTRING')
	#connection = cx_Oracle.connect(un, pw, cs)
        #with open('/etc/secrets/database/app_password, 'r') as secret_file:
        #pw = secret_file.read()

	connection = cx_Oracle.connect("SSB", "Ora_DB4U", "129.146.115.121/orclpdb")

	cursor = connection.cursor()
	cursor.execute("select systimestamp from dual")
	r, = cursor.fetchone()
	print(r)

	port = int(os.environ.get('PORT', 8080))
	run(host='0.0.0.0', port=port, debug=True)
