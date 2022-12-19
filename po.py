from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml
from yaml import load

app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']



mysql = MySQL(app)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        first_name = userDetails['first_name']
        last_name = userDetails['last_name']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO po_home(first_name, last_name, email, password) VALUES(%s, %s, %s, %s)', (first_name, last_name, email, password))
        mysql.connection.commit()
        cur.close()

    return render_template('home.html')

@app.route('/workon_approval', methods=['GET','POST'])
def workon_approval():
    if request.method == 'POST':
        userDetails = request.form
        work_number = userDetails['work_number']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO po_workon(work_number) VALUES(%s)',(work_number, ))
        mysql.connection.commit()
        cur.close()
    return render_template('workon_approval.html')

@app.route('/po_release', methods=['GET','POST'])
def po_release():
    if request.method == 'POST':
        userDetails = request.form
        po_number = userDetails['po_number']
        po_creation_date = userDetails['po_creation_date']
        po_valid_date = userDetails['po_valid_date']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO po_release(po_number, po_creation_date, po_valid_date) VALUES(%s, %s, %s)', (po_number, po_creation_date, po_valid_date))
        mysql.connection.commit()
        cur.close()
    return render_template('po_release.html')


if __name__ == '__main__':
    app.run(debug=True)