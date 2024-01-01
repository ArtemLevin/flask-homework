from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("age_verification.html")


@app.post('/age_verification/')
def calculate():
    name = request.form['name']
    age = request.form['age']
    if int(age) > 17:
        return redirect(url_for('verification_passed', name=name, age=age))
    return redirect(url_for('verification_blocked', name=name))


@app.route('/verification_passed/<age>/<name>')
def verification_passed(age, name):
    return render_template('verification_passed.html', name=name, age=age)

@app.route('/verification_blocked/<name>')
def verification_blocked(name):
    return render_template('verification_blocked.html', name=name)


if __name__ == '__main__':
    app.run()