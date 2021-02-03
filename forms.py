from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, email, ValidationError

class RegisterForm(FlaskForm):

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
  

    def validate_first_name(form, field):
        if (len(field.data) > 30):
            raise ValidationError('First Name must be 30 or lower characters')

    def validate_last_name(form, field):
        if (len(field.data) > 30):
            raise ValidationError('Last Name must be 30 or lower characters')

    def validate_email(form, field):
        if (len(field.data) > 50):
            raise ValidationError('Email must be 50 or lower characters')

    def validate_username(form, field):
        if (len(field.data) > 20):
            raise ValidationError('Username must less than 20 characters')

