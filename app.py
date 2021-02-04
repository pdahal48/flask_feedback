from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():

    form = RegisterForm()

    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        flash(f'Welcome {first_name}!')
        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/users/<username>')
def secret_page(username):

    if 'username' not in session:
        return redirect('/login')


    user = User.query.filter_by(username=username).first()
    feedbacks = Feedback.query.filter_by(username=username)

    return render_template('secret.html', user=user, feedbacks=feedbacks)


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f'Greetings {user.first_name}!')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid Username/password']
        
    return render_template('login.html', form=form)


#its better to make a logout a post request. Just add an empty form
@app.route('/logout', methods=['GET', 'POST'])
def logout_user():

    flash(f'You been logged out')
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>/feedbacks/add', methods=['GET', 'POST'])
def add_feedback(username):

    if 'username' not in session:
        return redirect('/login')
    
    # user = User.query.filter_by(username=username).first()
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feed = Feedback(title=title, content=content, username=username)
        db.session.add(feed)
        db.session.commit()
        flash('Feed Add Successful!')
        return redirect(f'/users/{username}')

    return render_template('feedback.html', form=form)
