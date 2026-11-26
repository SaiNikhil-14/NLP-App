from flask import Flask, render_template, request
from database import Database   #The class which we created

db = Database()
app = Flask(__name__)       #object of the Flask class

#We are creating routes(URL)
@app.route('/')     #Decorator
def index():
    #We are sending this to client
    return render_template('login.html')

#This triggers when we click /register next to the url.
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration', methods=['post'])
def perfrom_reg():
    name = request.form.get('usr_name')
    email = request.form.get('usr_email')
    password = request.form.get('usr_password')
    response = db.insert(name, email, password)

    if response:
        return "Registration Successful"
    else:
        return "Email already exists"

@app.route('/Verify', methods=['post'])
def verify():
    email = request.form.get('entered_email')
    password = request.form.get('entered_password')
    

app.run(debug=True)     #By keeping debug=True, no need to hit run button again and again