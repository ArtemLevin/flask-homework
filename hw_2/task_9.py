from flask import Flask, render_template, redirect, url_for, request, flash, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("name_and_email_input.html")


@app.post('/set_cookie/')
def set_cookie():
    context = {
        'username': request.form['username'],
        'email': request.form['email']
    }
    response = make_response(render_template('welcome_task_9.html', username=context['username']))
    response.set_cookie('username', context['username'])
    response.set_cookie('email', context['email'])
    return response


@app.route('/welcome_task_9/<username>')
def welcome_task_9(username):
    return render_template('welcome_task_9.html', username=username)


@app.route('/delete_cookies')
def delete_cookies():
    response = make_response(render_template('name_and_email_input.html'))
    response.set_cookie('username', 'None')
    response.set_cookie('email', 'None')
    return response


if __name__ == '__main__':
    app.run()
