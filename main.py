from flask import Flask,render_template,redirect,url_for,request,session,flash
import jinja2
import os
from Identifier import predict
from werkzeug.utils import secure_filename
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv("DATABASE_HOST")
DB_PASS = os.getenv("DATABASE_PASSWORD")

try:
    mydb =mysql.connector.connect(host=DB_HOST,user="pashudhan_habitlucky",passwd=DB_PASS,database="pashudhan_habitlucky",port="61002")
    cursor=mydb.cursor()
except:
    pass

def connectsql():
    try:
        mydb =mysql.connector.connect(host=DB_HOST,user="pashudhan_habitlucky",passwd=DB_PASS,database="pashudhan_habitlucky",port="61002")
        cursor=mydb.cursor()
    except Error as e:
        print(" MySQL Connection Failed:", e)


app = Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET_KEY","fallback_secret")
@app.route("/")
def home():
    if('user' in session):
        return render_template('index.html',status='Logout')
    else:
        return render_template('index.html',status='Login')
@app.route("/contact")
def contact():
    if('user' in session):
        return render_template('contact.html',status='Logout')
    else:
        return render_template('contact.html',status='Login')
@app.route("/login")
def login():
    if mydb.is_connected():
        pass
    else:
        connectsql()
    return render_template('login.html',status="Login")

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("home"))


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['usrid']
    password = request.form['password']
    try:
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
    except:
        pass
    return redirect(url_for('login'))
    
@app.route("/register")
def register():
    if 'user' in session:
        return render_template('register.html')
    else:
        return redirect(url_for('login'))

@app.route('/registeranimal',methods=['POST'])
def registeranimal():
    dr_id=session['user']
    entrydate=request.form['entrydate']
    taggingdate=request.form['taggingdate']
    species=request.form['species']
    name=request.form['name']
    sex=request.form['sex']
    dob=request.form['dob']
    tagno=request.form['eartag']
    try:

        sql = "INSERT INTO registered_animals (dr_id, entrydate, taggingdate,species,name,sex,dob,tagno) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        values = (dr_id, entrydate, taggingdate,species,name,sex,dob,tagno)

        cursor.execute(sql, values)
        mydb.commit()
    except:
        pass
    return redirect(url_for('home'))


@app.route("/identify")
def identify():
    if 'user' in session:
        return render_template('identify.html',breed="",status="Logout")
    else:
        return render_template('identify.html',breed="",status="Login")


@app.route("/identifyanimal",methods=['POST'])
def identifyanimal():
    if 'image' not in request.files:
        return "No file part"

    file = request.files['image']

    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    temp_path = os.path.join("temp_uploads", filename)
    
    os.makedirs("temp_uploads", exist_ok=True)
    
    file.save(temp_path)
    predicted_class= predict(img_path=temp_path)

    os.remove(temp_path)
    if 'user' in session:
        return render_template('identify.html',breed=f"Identified breed: {predicted_class}",status="Logout")
    else:
        return render_template('identify.html',breed=f"Identified breed: {predicted_class}",status="Login")



@app.route("/search")
def search():
    if 'user' in session:
        return render_template('search.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(host="0.0.0.0.",port=5000)
