from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegistrationForm
from models import User, Post

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

@app.cli.command("add-john")
def add_user():
    user = User(username='john', email='lolkek@gmail.com')
    db.session.add(user)
    db.session.commit()
    print('John successfully added to the database')

@app.cli.command("edit-john")
def edit_user():
    user=User.query.filter_by(username='john').first()
    user.email = 'newlolkek@gmail.com'
    print('Edit John mail in database')

@app.cli.command('del-john')
def del_user():
    user = User.query.filter_by(username='John').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete John from database')

@app.route('users/<username>/')
def users_by_username(username):
    users=User.query.filter(User.username == username).all()
    context = {'users':users}
    return render_template('users.html', **context)

@app.route('/posts/author/<int:user_id>/')
def get_posts_by_author(user_id):
    posts = Post.query.filter_by(author_id=user_id).all()
    if posts:
        return jsonify(
            [{'id': post.id, 'title': post.title, 'content': post.content, 'create_at': post.created_at} for post in posts]
        )
    else:
        return jsonify({'error':' Post not found'}), 404

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        pass
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        print(email, password)
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

