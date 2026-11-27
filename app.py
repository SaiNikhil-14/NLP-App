from flask import Flask, render_template, request, redirect
#Here render_template is used for returning the html file
#request is used for getting the data from a file.
#redirect is used for returning another route
from database import Database   #The class which we created
import api

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
        return render_template('login.html', message='Registration successful. Kindly login here.', color='green')
    else:
        return render_template('register.html', message='Email already exists')

@app.route('/perform_login', methods=['post'])
def perform_login():
    email = request.form.get('entered_email')
    password = request.form.get('entered_password')

    response = db.search(email, password)
    if response:
        return redirect('/profile')     #returning another route
    else:
        return render_template('login.html', message='Invalid credentials!', color='red')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/ner')
def ner():
    return render_template('ner.html')

@app.route('/perform_ner', methods=['post'])
def perform_ner():
    text = request.form.get('ner_text')
    response = api.extract_entities(text)
    json_output = response.model_dump()
    return render_template('ner.html', response=json_output)


app.run(debug=True)     #By keeping debug=True, no need to hit run button again and again
