from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
users = {
    'user1': 'pwd1',
    'user2': 'pwd2',
}


@app.route("/")
def index():
    return render_template("login.html")


@app.post('/login/')
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return redirect(url_for('welcome', username=username))
    return redirect(url_for('block'))


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


@app.route('/block/')
def block():
    return render_template('block.html')


if __name__ == "__main__":
    app.run()
