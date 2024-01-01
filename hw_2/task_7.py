from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("num_input_page.html")


@app.post('/num_input/')
def squaring():
    num = request.form['num']
    return redirect(url_for('squaring_result', result=str(int(num)**2)))


@app.route("/squaring_result/<result>")
def squaring_result(result):
    return render_template('squaring_result.html', result=result)

if __name__ == '__main__':
    app.run()