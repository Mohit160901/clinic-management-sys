from flask import Blueprint, Flask, render_template ,request,flash,jsonify,redirect,url_for
from flask_login import login_user, login_required , current_user
from .models import Note,appointment,User
from . import db
import  json

#from . import  mail ,Message



views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/login_home', methods=['GET','POST'])
@login_required
def login_home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        message = request.form.get('message')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email are not same. ', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 character.', category='error')

        elif len(name) < 2:
            flash('First name must be greater than 1  character.', category='error')

        elif len(message) < 1:
            flash('Message should be more than 1 character', category='error')

        elif len(phone) < 7:
            flash('Phone number must be more than that it should be up to 10', category='error')

        else:
            new_appoint = appointment(name=name,email=email,phone=phone,appointment_date=date,message=message,user_id=current_user.id)
            db.session.add(new_appoint)
            db.session.commit()

            flash('Appointment made you will hear from us shortly!!', category='success')
            return redirect(url_for('views.login_home'))

    return render_template("user_home.html")


@views.route('/information_insertion', methods=['GET','POST'])
def information_insertion():
    if request.method == "POST":
        note = request.form.get('note')

        if  len(note) < 1:
            flash('information description is short !!!', category='error')

        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash('Information Added!!', category='success')
    return render_template('info.html', user=current_user)


@views.route('/Doctor_page')
def Doc_pg():
   # appointment = request.data('appointment')
    temp = appointment.query.all()
    temp2 = Note.query.all()
    return render_template('Docmain.html', appoint=temp, info = temp2 )


@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)

    noteId= note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
