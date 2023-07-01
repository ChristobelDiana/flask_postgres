import psycopg2
from flask import Flask,render_template, request,redirect,url_for

app = Flask(__name__)


def db_conn():
    conn = psycopg2.connect(database="flask_db", host="localhost", user="postgres", password="godsgift", port="5432")
    return conn


@app.route('/')
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM courses ORDER BY id''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html',data= data)


@app.route('/create',methods=['POST'])
def create():
    conn=db_conn()
    cur = conn.cursor()
    name = request.form['name']
    fees = request.form['fees']
    duration = request.form['duration']
    cur.execute('''INSERT INTO courses (name,fees,duration) VALUES(%s,%s,%s)''',(name,fees,duration))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cur = conn.cursor()

    name = request.form['name']
    fees = request.form['fees']
    duration = request.form['duration']
    id = request.form['id']

    cur.execute(
		'''UPDATE courses SET name=%s,fees=%s, duration=%s WHERE id=%s''', (name, fees,duration, id))


    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cur = conn.cursor()

    # Get the data from the form
    id = request.form['id']

    # Delete the data from the table
    cur.execute('''DELETE FROM courses WHERE id=%s''', (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))
