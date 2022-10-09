from flask import Blueprint, render_template , request , flash , url_for,redirect
from .models import User , Doctor
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required , current_user ,logout_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash('Loggin Successfully !', category='success')
                login_user(user , remember=True)
                return redirect(url_for('views.login_home'))
            else:
                flash('Loggin Unsuccessfully !', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))






@auth.route('/doctor_login',methods=['GET', 'POST'])
def doctor_login():

  #  doc1 = Doctor(email='Doctor1@gmail.com', password = generate_password_hash(password,method='sha256'))
       # temp = True

    #    doc1 = Doctor(email='Doctor1@gmail.com', password = generate_password_hash(password,method='sha256'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # doc1 = Doctor(email='Doctor25@gmail.com', password=generate_password_hash(password, method='sha256'))
        # db.session.add(doc1)
        # db.session.commit()

        user1 = Doctor.query.filter_by(email=email).first()

        if user1:
            if check_password_hash(user1.password,password):
                flash('Loggin Successfully !', category='success')
                #login_user(user1 , remember=True)
                return redirect(url_for('views.Doc_pg'))
            else:
                flash('Loggin Unsuccessfully !', category='error')
    return render_template("doctor_login.html")




@auth.route('/patient_signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists. ', category='error')

        elif len(email) <  4:
            flash('Email must be greater than 3 character.', category= 'error')

        elif len(first_name) < 2 :
            flash('First name must be greater than 1  character.', category='error')
        
        elif  password1 != password2:
            flash('Passwords dont\'t match.', category='error')
        
        elif  len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        
        else:
            new_user = User(email=email,first_name=first_name, password = generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
           # login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.Doc_pg'))
            

    return render_template("sign_up.html")




