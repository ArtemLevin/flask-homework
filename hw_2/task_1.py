from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/greet', methods=['POST'])
def greet():
    username = request.form['username']
    return render_template("greet.html", username=username)


if __name__ == '__main__':
    app.run()
