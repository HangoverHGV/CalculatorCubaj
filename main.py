import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine
import math


app = Flask(__name__)

DB_user='calculatorCubaj'
DB_pass='calculator123'
DB_host='localhost'
DB_name='cubajdb'

uri = 'mysql+pymysql://'+ DB_user +':'+ DB_pass +'@'+ DB_host +'/'+ DB_name

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "banana123"

mysql = SQLAlchemy(app)

class Rezultate(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key = True)
    lungime = mysql.Column(mysql.String(50))
    diametru = mysql.Column(mysql.String(50))
    volumul = mysql.Column(mysql.String(50))


tblname = Rezultate().__class__.__name__

engine = create_engine(uri)
def GetTableByName():
    exists = False
    tables = inspect(engine)
    for t_name in tables.get_table_names():
        if(t_name == tblname):
            exists = True
            break
        else:
            exists = False

    return exists

if GetTableByName() == False:
    mysql.create_all()

vol = 0
alert = False
@app.route('/')
def index():
    total = 0
    result = Rezultate.query.all()
    if alert == True:
        flash('AAAA', category='error')

    for i in result:
        total += float(i.volumul)
    
    return render_template('index.html', result=result, volum = vol, total = round(total, 3))

@app.route('/process', methods = ['POST'])
def process():
    global vol
    global alert
    lungime = request.form['lungime']
    diametru = request.form['diametru']
    if lungime.isdigit() and diametru.isdigit():
        dimensions = Rezultate(lungime = lungime, diametru = diametru, volumul = Volum(lungime, diametru))
        mysql.session.add(dimensions)
        mysql.session.commit()
        vol = Volum(lungime, diametru)
    else:
        alert = True
    return redirect(url_for('index'))
    
    

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    row_to_delete = Rezultate.query.get(id)
    mysql.session.delete(row_to_delete)

    mysql.session.commit()
    return redirect(url_for('index'))




#Mathematics 
pi = math.pi

def Volum(lng,d):
    r = float(d)/200
    l = float(lng)

    v = pi *(r**2) *l

    return round(v,3) 

if __name__=="__main__":
    app.run(host='0.0.0.0', port = 8080, debug=True)