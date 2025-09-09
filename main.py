from flask import Flask,render_template,redirect,url_for,request
import jinja2
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/login")
def login():
    return render_template('login.html')
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['usrid']
    password = request.form['password']
    return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(debug=True)