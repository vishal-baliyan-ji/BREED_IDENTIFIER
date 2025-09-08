from flask import Flask,render_template
import jinja2
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
   app.run(debug=True)