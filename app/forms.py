from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.qa.qa import DEFAULT_CONTEXT, DEFAULT_QUESTION

class QAForm(FlaskForm):

  context = TextAreaField(
    "Context",
    default=DEFAULT_CONTEXT,
    validators=[DataRequired()]
  )
  question = StringField(
    "Question",
    default=DEFAULT_QUESTION,
    validators=[DataRequired()]
  )
  submit = SubmitField('Submit')
  
  def __init__(self):
    super(QAForm, self).__init__()


class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField('Submit')

class SignupForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
  submit = SubmitField('Submit')
