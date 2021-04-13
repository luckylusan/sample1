from flask import Flask, render_template
from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///google_forms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class GoogleForms(db.Model):
    __tablename__ = "google_forms"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    contact = db.Column(db.Integer)
    email = db.Column(db.String(200))
    gender = db.Column(db.String(200))
    subject = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)




from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect

app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)



csrf = CSRFProtect()

csrf.init_app(app)

@app.route('/')
def home():
    # return render_template('GoogleForm/index.html')
    return render_template('GoogleForm/createForm.html')

@app.route('/createform')
def createForm():
    return render_template('GoogleForm/createForm.html')


@app.route('/saveForm', methods=['GET', 'POST'])
def saveForm():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        gender = request.form['gender']
        subject = str(request.form.getlist('subject'))
        print(subject)

        data = GoogleForms(name=name, contact=contact, email=email, gender=gender, subject=subject)
        db.session.add(data)
        db.session.commit()

        all_forms = GoogleForms.query.all()

        return render_template('view_form.html',all_forms=all_forms)


@app.route('/formsList', methods=['GET', 'POST'])
def formsList():
    all_forms = GoogleForms.query.all()
    return render_template('view_form.html', all_forms=all_forms)


@app.route('/editForm/<int:sno>', methods=['GET', 'POST'])
def editForm(sno):
    ed_form = GoogleForms.query.filter_by(sno=sno)
    return render_template('edit_form.html', ed_form=ed_form)


@app.route('/updateForm/<int:sno>', methods=['GET', 'POST'])
def updateForm(sno):

    name = request.form['name']
    contact = request.form['contact']
    email = request.form['email']
    gender = request.form['gender']
    subject = request.form['subject']

    ed_form = GoogleForms.query.filter_by(sno=sno).first()
    ed_form.name=name
    ed_form.contact = contact
    ed_form.email = email
    ed_form.gender = gender
    ed_form.subject = subject
    db.session.add(ed_form)
    db.session.commit()
    return redirect('/formsList')

@app.route('/deleteForm/<int:sno>', methods=['GET', 'POST'])
def deleteForm(sno):
    ed_form = GoogleForms.query.filter_by(sno=sno).first()
    db.session.delete(ed_form)
    db.session.commit()
    return redirect('/formsList')



@app.route('/products', methods=['GET', 'POST'])
def products():
    return 'this is products page!'




if __name__ == "__main__":
    app.run()