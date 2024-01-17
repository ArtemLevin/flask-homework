from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm
from models import User
from hashlib import sha256
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://mydatabase.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Hi!'

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/', methods=['GET','POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    surname=form.username.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

