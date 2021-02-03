from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text(30), nullable=False)
    last_name = db.Column(db.Text(30), nullable=False)
    email = db.Column(db.Text(50), nullable=False, unique=True)
    username = db.Column(db.Text(20), nullable=False)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """ Register user w/hashed password and return the user itself """

        hashed = bcrypt.generate_password_hash(password)

        #turn the bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

    @classmethod
    def authenticate(cls, username, password):
        """ returns user if user exists and password matches """
        
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete='Cascade'))
    