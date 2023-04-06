from flask import render_template, flash, redirect
from flask import session, url_for
from app import app
from app.forms import QAForm, LoginForm, SignupForm
from app.qa.qa import QuestionAnswerer
import psycopg2.pool
import os
import bcrypt

answerer = QuestionAnswerer()

class DBConn(object):

  def __init__(self, min_size=0, max_size=80):
    self.pool = psycopg2.pool.SimpleConnectionPool(
      min_size,
      max_size,
      os.environ["DATABASE_URL"]
    )
    self.conn = self.pool.getconn()
    self.cursor = self.conn.cursor() 
    self.conn.autocommit = True

  def close_connection(self):
    self.pool.putconn(self.conn)
    self.conn.close()
  
  def store_query(self, context, question, answer):
    command = "insert into queries (user_id, name, lang_code, created, question, context, answer) values (1, '', 'it', now(), %s, %s, %s)"
    self.cursor.execute(command, (question, context, answer))

  def get_user_queries(self, user_id, limit=5):
    command = "select question, answer from queries where user_id = %s order by created DESC limit %s"
    self.cursor.execute(command, (user_id, limit,))
    return QAList(self.cursor.fetchall())

  def password_matches(self, password, username):
    command = "select hash from users where email = %s"
    self.cursor.execute(command, (username,))
    fetch = self.cursor.fetchone()
    if fetch is None:
      raise Exception("Username not found")
    hash = fetch[0]
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

  def add_user(self, username, password):
    hash = hash_password(password)
    command = "insert into users (name, email, hash) values (%s, %s, %s)"
    self.cursor.execute(command, ("", username, hash))

class QAItem(object):

  def __init__(self, question, answer):
    self.question = question
    self.answer = answer

class QAList(object):

  def __init__(self, records=None):
    if not records is None:
      self.items = [QAItem(record[0], record[1]) for record in records]
    else:
      self.items = []

  def __iter__(self):
    return self.items.__iter__()

def hash_password(password):
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password.decode('utf-8')



db = DBConn()

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    user_id = session.get('user_id')
    print(f"user_id:{user_id}")
    form = QAForm()
    if form.validate_on_submit():
        try: # Generate answer and store record
          answer = answerer.answer_question(
            form.context.data,
            form.question.data
          )
          db.store_query(form.context.data, form.question.data, answer)
        except Exception as e:
          return render_template('error.html', error=e)
        records = db.get_user_queries(1)
        return render_template(
          "index.html",
          title="Home",
          form=form,
          answer=answer,
          records=records
        )
    else:
        records = db.get_user_queries(1)
        return render_template(
          "index.html",
          title="Home",
          form=form,
          default_question=answerer.default_question,
          default_context=answerer.default_context,
          records=records
        )

@app.route('/login', methods=["GET"])
def login_get():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route('/login', methods=["POST"])
def login_post():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      if db.password_matches(form.password.data, form.username.data):
        return redirect("/")
      else:
        flash("Invalid password, please try again.")
        return render_template("login.html", title="Login", form=form)
    except Exception as e:
       flash("An error occurred while processing your request: " + str(e))
       return render_template("login.html", title="Login", form=form)
  return render_template('error.html', error="Invalid form submission")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            db.add_user(form.username.data, form.password.data)
        except Exception as e:
            return render_template('error.html', error=e)
        return redirect(url_for('login_get'))
    else:
        for field, errors in form.errors.items():
          for error in errors:
            flash("%s: %s" % (getattr(form, field).label.text, error), "error")
        return render_template("signup.html", title="Signup", form=form)