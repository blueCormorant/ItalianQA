from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
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

  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    self.submit.label.text = "Sign up"
  
  def validate_confirm_password(form, field):
    if field.data != form.password.data:
      raise ValidationError("Passwords must match")
    
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), validate_confirm_password])
  submit = SubmitField('Submit')
  