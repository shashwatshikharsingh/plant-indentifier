import json
import cv2
from flask import Flask, flash, redirect, render_template, request, session,g,jsonify,url_for
from flask_session import Session
from tempfile import mkdtemp
import numpy as np
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import random
from helpers import apology, login_required
import logging
import joblib




app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_path = '/static/svm_model_update.pkl'

def extract_hog_features(image):
    image = cv2.resize(image, (64, 128))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hog = cv2.HOGDescriptor()
    features = hog.compute(gray)
    return features.flatten()

model_filename = "./static/svm_model_update.pkl"
loaded_model = joblib.load(model_filename)

with open('plants.json', 'r') as json_file:
    plant_data = json.load(json_file)


def get_db():
    """Open a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect("ayurveda_users.db")
        g.sqlite_db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hash TEXT NOT NULL)")
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/",methods=["GET"])
@login_required
def index():
    """Main Page"""
    return render_template("index.html")



@app.route('/upload', methods=['POST'])
def upload():
    try:
        if request.method == 'POST':

            if 'image' not in request.files:
                return apology("No file part", 400)

            image_file = request.files['image']

            if image_file.filename == '':
                return apology("No selected file", 400)

            allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
            if '.' not in image_file.filename or image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return apology("Invalid file format", 400)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            image_file_name = str(session["user_id"])  + str(random.randint(1,1000000)) + image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file_name)

            # Save the file
            image_file.save(image_path)

            with open(image_path, 'rb') as file:
                image_data = file.read()

            
            nparr = np.frombuffer(image_data, np.uint8)
            image_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            test_features = extract_hog_features(image_cv2)

            result = loaded_model.predict([test_features])
            predicted_label = result[0].lower()
            print(predicted_label)
            session["plant_name"] = predicted_label
            return jsonify({'result': predicted_label})
    except Exception as e:
        logging.error(str(e))
        return apology("Internal Server Error", 500)
    
 
@app.route("/info/<plant_name>",methods=["GET"])
def info(plant_name):
    if request.method == "GET":
      
        plant_info = None
        for plant in plant_data['plants']:
            if plant['name'] == plant_name:
                plant_info = plant
                break
        if plant_info:
            return render_template('info.html', plant_name=plant_info['name'], plant_image=plant_info["image_url"], history=plant_info['History'], location=plant_info['Location'], soil=plant_info['Soil'],medicinal_value=plant_info["MedicinalValue"])
        else:
            return apology("Plant information not found", 404)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0][0]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please Enter a Username")
        if not password or not confirmation or password != confirmation:
            return apology("Please correctly write both password fields")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        duplicate = cursor.fetchone()

        if duplicate:
            return apology("Username already exists")

        passwordHash = generate_password_hash(password)

        cursor.execute("INSERT INTO users (username,hash) VALUES (?, ?)", (username, passwordHash))
        db.commit()

        return redirect("/login")

    else:
        return render_template("register.html")
