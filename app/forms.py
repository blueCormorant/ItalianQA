from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class QAForm(FlaskForm):    
    context = StringField("Context", validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):    
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')
