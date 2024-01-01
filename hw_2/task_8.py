from flask import Flask, render_template, redirect, url_for, request, flash


app = Flask(__name__)
app.secret_key =b'8559823b002d109d02c548497f9ba8a6ca4a423b8f2acc5cc73959fc6dd44821'


@app.route("/")
def index():
    return render_template("name_input.html")

@app.route('/name_input')
def name_input():
    return redirect('form')


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        flash(f'Привет, {request.form["name"]}!')
        return render_template("form.html")


if __name__ == '__main__':
    app.run()