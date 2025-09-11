from flask import Flask,render_template,redirect,url_for,request,session,flash
import jinja2


import mysql.connector
mydb =mysql.connector.connect(host="localhost",user="root",passwd="Roomno775",database="pashudhan")

cursor=mydb.cursor()


app = Flask(__name__)
app.secret_key="raja-moli"
@app.route("/")
def home():
    if('user' in session):
        return render_template('index.html',status='Logout')
    else:
        return render_template('index.html',status='Login')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/login")
def login():
    return render_template('login.html',status="Login")

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("home"))


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['usrid']
    password = request.form['password']
    sql="select password, name from drs_data where id=%s"
    cursor.execute(sql,(username,))
    data=cursor.fetchone()
    pwd=data[0]
    name=data[1]
    if (password==pwd):
        session['user']=username
        session['name']=name
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))
    
@app.route("/register")
def register():
    if 'user' in session:
        return render_template('register.html')
    else:
        return redirect(url_for('login'))

@app.route('/registeranimal',methods=['POST'])
def registeranimal():
    return redirect(url_for('home'))


@app.route("/identify")
def identify():
    return render_template('identify.html')


@app.route("/identifyanimal",methods=['POST'])
def identifyanimal():
    return redirect(url_for('identify'))


@app.route("/search")
def search():
    if 'user' in session:
        return render_template('search.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug=True)