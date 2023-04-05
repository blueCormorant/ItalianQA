from flask import render_template, flash, redirect
from flask import session
from app import app
from app.forms import QAForm, LoginForm
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

  def password_matches(self, password, user_id):
    command = "select hash from users where id = %s"
    self.cursor.execute(command, (user_id,))
    hash = self.cursor.fetchone()[0]
    print(password.encode('utf-8') , hash.encode('utf-8'))
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

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

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Hash:{hash_password(form.password.data)}")
        if db.password_matches(form.password.data, 1):
            session['1'] = 1
            return redirect("/")
        else:
            return render_template("login.html", form=form)
    return render_template("login.html", title="Login", form=form)