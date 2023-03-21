from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Api
import qrcode
import io
import pybase64
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'Ironman@2'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/waste_mangement_system'
db = SQLAlchemy(app)
api = Api(app)

model = load_model('waste_classifier.h5')

# classes = {0: 'Organic Waste', 1: 'Recyclable Waste'}

def preprocess_image(image_path):
    # Load the image and convert it to a numpy array
    img = load_img(image_path, target_size=(64, 64))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Preprocess the image
    # img_array /= 255.
    return img_array

class userdata(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    d1 = db.Column(db.Integer, nullable=True)
    d2 = db.Column(db.Integer, nullable=False)
    d3 = db.Column(db.Integer, nullable=False)
    d4 = db.Column(db.Integer, nullable=False)
    d5 = db.Column(db.Integer, nullable=False)
    d6 = db.Column(db.Integer, nullable=False)
    d7 = db.Column(db.Integer, nullable=False)
    d8 = db.Column(db.Integer, nullable=False)
    d9 = db.Column(db.Integer, nullable=False)
    d10 = db.Column(db.Integer, nullable=False)
    d11 = db.Column(db.Integer, nullable=False)
    d12 = db.Column(db.Integer, nullable=False)
    d13 = db.Column(db.Integer, nullable=False)
    d14 = db.Column(db.Integer, nullable=False)
    d15 = db.Column(db.Integer, nullable=False)
    d16 = db.Column(db.Integer, nullable=False)
    d17 = db.Column(db.Integer, nullable=False)
    d18 = db.Column(db.Integer, nullable=False)
    d19 = db.Column(db.Integer, nullable=False)
    d20 = db.Column(db.Integer, nullable=False)
    d21 = db.Column(db.Integer, nullable=False)
    d22 = db.Column(db.Integer, nullable=False)
    d23 = db.Column(db.Integer, nullable=False)
    d24 = db.Column(db.Integer, nullable=False)
    d25 = db.Column(db.Integer, nullable=False)
    d26 = db.Column(db.Integer, nullable=False)
    d27 = db.Column(db.Integer, nullable=False)
    d28 = db.Column(db.Integer, nullable=False)
    d29 = db.Column(db.Integer, nullable=False)
    d30 = db.Column(db.Integer, nullable=False)
    d31 = db.Column(db.Integer, nullable=False)
    orgp = db.Column(db.Float, nullable=True)
    recp = db.Column(db.Float, nullable=True)
    incentive = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(100), nullable=True)

class garbagecollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.name'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pending')

class contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(100), nullable=True)
    complain = db.Column(db.String(500), nullable=True)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/preeds")
def preeds():
    return render_template('predict.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    # Get the uploaded file
    image_file = request.files['image']
    # Save the file to a temporary directory
    temp_dir = os.path.join(app.root_path, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, image_file.filename)
    image_file.save(temp_path)
    # Preprocess the image
    img_array = preprocess_image(temp_path)
    # Make a prediction
    prediction = model.predict(img_array)
    # Get the class label
    if prediction[0][0] == 1:
        class_label = "Recyclable Waste"
    else:
        class_label = "Organic Waste"
    # class_id = np.argmax(prediction[0])
    # class_label = classes[class_id]
    # Return the result
    return render_template('predict.html',class_label=class_label)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        address = request.form.get('address')
        entry = userdata(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email, address=address )
        db.session.add(entry)
        db.session.commit()
        session['name']=name
        return redirect(url_for('user_home'))
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form.get('name')
        message=request.form.get('message')
        user=userdata.query.filter_by(name=name,msg=message).first()
        if user:
            session['name']=name
            return redirect(url_for('user_home'))
        else:
            return render_template('login.html',error='Invalid Username or Password')
    return render_template('login.html')

@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if 'name' not in session:
        return redirect(url_for('login'))
    # order_by(garbagecollection.date.asc()).all()
    user = userdata.query.filter_by(name=session['name']).first()
    garbage_collections = garbagecollection.query.filter_by(user_id=user.name).first()
    gc = garbagecollection.query.filter_by(user_id=user.name).all()
    org = 1
    rec = 1
    for use in gc:
        if use.type=="recycle":
            rec+=1
        elif use.type=="organic":
            org+=1
    tot=rec+org
    orgpe = (org/tot) * 100
    recp = (rec/tot)*100

    user.recp = recp
    user.orgp = orgpe
    if recp < orgpe :
        inc=(recp/orgpe)*tot
        inc=round(inc)
        user.incentive = inc
    else:
        inc=(orgpe/recp)*tot
        inc = round(inc)
        user.incentive = inc

    if request.method == 'POST':
        date_str= request.form.get('date')
        date = datetime.strptime(date_str, '%d/%m/%y').date()
        type = request.form.get('type')
        setattr(user, 'd' + str(date.day), 1)

        garbage_collection = garbagecollection(user_id=user.name, date=date, type=type)
        db.session.add(garbage_collection)
        db.session.commit()
        return redirect(url_for('user_home'))

    # Generate the QR code image using the user's id
    qr = qrcode.QRCode(version=None, box_size=10, border=5)
    qr.add_data(user.name)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to base64 string for displaying in HTML
    buffer = io.BytesIO()
    img.save(buffer)
    img_binary = buffer.getvalue()
    img_str = pybase64.b64encode(img_binary).decode()

    return render_template('user_home.html',garbage_collections=garbage_collections,user=user,qr_code=img_str)

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        usern=request.form.get('usern')
        passw=request.form.get('passw')
        if ((usern == "admin") and (passw =="ironman2")):
            print("Hello")
            session['gname']=usern
            return redirect(url_for('admin_home'))
        else:
            return render_template('admin.html',error='Invalid Username or Password')
    return render_template('admin.html')

@app.route('/admin_home',methods=['GET','POST'])
def admin_home():
    # print(session)
    if 'gname' not in session:
        return redirect(url_for('admin'))
    garbage_collections = garbagecollection.query.order_by(garbagecollection.date.asc()).all()
    return render_template('admin_home.html',garbage_collections=garbage_collections)

@app.route('/approve', methods=['GET','POST'])
def approve():
    if 'gname' not in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        garbage_collection_id = request.form.get('garbage_collection_id')
        garbage_collection = garbagecollection.query.filter_by(user_id=garbage_collection_id).all()
        for user in garbage_collection:
            user.status = 'Approved'

        # Get user and date of the garbage collection
        gc = garbagecollection.query.filter_by(user_id=garbage_collection_id).first()
        user_id = gc.user_id
        # collection_date = garbage_collection.date

        # Query the garbagecollection table for the user and date
        garbage_collection_for_user = userdata.query.filter_by(name=user_id).first()

        # Reset the values of d1, d2, d3, and so on to zero for that user and date
        if garbage_collection_for_user.d1 == 1:
            garbage_collection_for_user.d1 = 2
        if garbage_collection_for_user.d2 == 1:
            garbage_collection_for_user.d2 = 2
        if garbage_collection_for_user.d3 == 1:
            garbage_collection_for_user.d3 = 2
        if garbage_collection_for_user.d4 == 1:
            garbage_collection_for_user.d4 = 2
        if garbage_collection_for_user.d5 == 1:
            garbage_collection_for_user.d5 = 2
        if garbage_collection_for_user.d6 == 1:
            garbage_collection_for_user.d6 = 2
        if garbage_collection_for_user.d7 == 1:
            garbage_collection_for_user.d7 = 2
        if garbage_collection_for_user.d8 == 1:
            garbage_collection_for_user.d8 = 2
        if garbage_collection_for_user.d9 == 1:
            garbage_collection_for_user.d9 = 2
        if garbage_collection_for_user.d10 == 1:
            garbage_collection_for_user.d10 = 2
        if garbage_collection_for_user.d11 == 1:
            garbage_collection_for_user.d11 = 2
        if garbage_collection_for_user.d12 == 1:
            garbage_collection_for_user.d12 = 2
        if garbage_collection_for_user.d13 == 1:
            garbage_collection_for_user.d13 = 2
        if garbage_collection_for_user.d14 == 1:
            garbage_collection_for_user.d14 = 2
        if garbage_collection_for_user.d15 == 1:
            garbage_collection_for_user.d15 = 2
        if garbage_collection_for_user.d16 == 1:
            garbage_collection_for_user.d16 = 2
        if garbage_collection_for_user.d17 == 1:
            garbage_collection_for_user.d17 = 2
        if garbage_collection_for_user.d18 == 1:
            garbage_collection_for_user.d18 = 2
        if garbage_collection_for_user.d19 == 1:
            garbage_collection_for_user.d19 = 2
        if garbage_collection_for_user.d20 == 1:
            garbage_collection_for_user.d20 = 2
        if garbage_collection_for_user.d21 == 1:
            garbage_collection_for_user.d21 = 2
        if garbage_collection_for_user.d22 == 1:
            garbage_collection_for_user.d22 = 2
        if garbage_collection_for_user.d23 == 1:
            garbage_collection_for_user.d23 = 2
        if garbage_collection_for_user.d24 == 1:
            garbage_collection_for_user.d24 = 2
        if garbage_collection_for_user.d25 == 1:
            garbage_collection_for_user.d25 = 2
        if garbage_collection_for_user.d26 == 1:
            garbage_collection_for_user.d26 = 2
        if garbage_collection_for_user.d27 == 1:
            garbage_collection_for_user.d27 = 2
        if garbage_collection_for_user.d28 == 1:
            garbage_collection_for_user.d28 = 2
        if garbage_collection_for_user.d29 == 1:
            garbage_collection_for_user.d29 = 2
        if garbage_collection_for_user.d30 == 1:
            garbage_collection_for_user.d30 = 2
        if garbage_collection_for_user.d31 == 1:
            garbage_collection_for_user.d31 = 2
        db.session.commit()
        return redirect(url_for('admin_home'))

@app.route('/reset_home',methods=['GET','POST'])
def reset_home():
    if 'gname' not in session:
        return redirect(url_for('admin'))
    garbage_collections = garbagecollection.query.order_by(garbagecollection.date.asc()).all()
    return render_template('reset_home.html',garbage_collections=garbage_collections)

@app.route('/reset', methods=['GET','POST'])
def reset():
    if 'gname' not in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        garbage_collection_id = request.form.get('garbage_collection_id')
        garbage_collection = garbagecollection.query.filter_by(user_id=garbage_collection_id).first()
        user_id = garbage_collection.user_id
        garbage_collection_for_user = userdata.query.filter_by(name=user_id).first()
        garbage_collection_for_user.d1 = 0
        garbage_collection_for_user.d2 = 0
        garbage_collection_for_user.d3 = 0
        garbage_collection_for_user.d4 = 0
        garbage_collection_for_user.d5 = 0
        garbage_collection_for_user.d6 = 0
        garbage_collection_for_user.d7 = 0
        garbage_collection_for_user.d8 = 0
        garbage_collection_for_user.d9 = 0
        garbage_collection_for_user.d10 = 0
        garbage_collection_for_user.d11 = 0
        garbage_collection_for_user.d12 = 0
        garbage_collection_for_user.d13 = 0
        garbage_collection_for_user.d14 = 0
        garbage_collection_for_user.d15 = 0
        garbage_collection_for_user.d16 = 0
        garbage_collection_for_user.d17 = 0
        garbage_collection_for_user.d18 = 0
        garbage_collection_for_user.d19 = 0
        garbage_collection_for_user.d20 = 0
        garbage_collection_for_user.d21 = 0
        garbage_collection_for_user.d22 = 0
        garbage_collection_for_user.d23 = 0
        garbage_collection_for_user.d24 = 0
        garbage_collection_for_user.d25 = 0
        garbage_collection_for_user.d26 = 0
        garbage_collection_for_user.d27 = 0
        garbage_collection_for_user.d28 = 0
        garbage_collection_for_user.d29 = 0
        garbage_collection_for_user.d30 = 0
        garbage_collection_for_user.d31 = 0
        db.session.commit()
        return redirect(url_for('reset_home'))

@app.route('/contact', methods = ['GET', 'POST'])
def contact_form_submission():
    if (request.method == 'POST'):
        nam = request.form.get('name')
        emai = request.form.get('email')
        subjec = request.form.get('subject')
        messag = request.form.get('message')
        entry = contact(name=nam, email=emai, subject=subjec, complain=messag)
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html')


@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name')
    if 'gname' in session:
        session.pop('gname')
    return render_template('index.html')

