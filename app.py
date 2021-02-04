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
    """ Simply redirects to register page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """ Allows a user to register if condition meets else redirected to registration page """
    
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


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    ''' Authenticates and logs the user in'''

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


@app.route('/users/<username>')
def secret_page(username):
    """ Displays information regarding the user and their feeds. Allows to create new as well"""

    if 'username' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    feedbacks = Feedback.query.filter_by(username=username)

    return render_template('secret.html', user=user, feedbacks=feedbacks)



@app.route('/logout', methods=['POST'])
def logout_user():
    """ Logs out the user"""

    flash(f'You been logged out')
    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>/feedbacks/add', methods=['GET', 'POST'])
def add_feedback(username):
    """ Allows the user to add new feedbacks"""

    if 'username' not in session:
        return redirect('/login')
    
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


@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    """ Allows the user to update their feedback"""

    if 'username' not in session:
        return redirect('/login')

    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash(f"Feedback updated!")
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)


@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """ Deletes a feedback from the database"""

    if 'username' not in session:
        return redirect('/login')

    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    flash(f"Feedback Deleted!")
    return redirect(f"/users/{feedback.username}")


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """ Deletes the user from the database. feedbacks related are also deleted"""

    if 'username' not in session:   
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash("User Deleted!")
    return redirect(f"/")


    
