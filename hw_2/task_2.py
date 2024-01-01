from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


# @app.route('/')
# def index():
#     return f'Main page'


@app.route('/')
def page():
    context = {'title': 'Any page'}
    return render_template('page.html', **context)


@app.route('/upload')
def upload():
    return render_template('upload.html')


if __name__ == "__main__":
    app.run()
