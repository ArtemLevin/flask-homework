from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("text.html")


@app.post('/text/')
def login():
    text = request.form['text']
    return redirect(url_for('lenText', text=text))


@app.route('/len/<text>')
def lenText(text):
    return render_template('lenText.html', lenText=len(text.split(" ")))


if __name__ == '__main__':
    app.run()