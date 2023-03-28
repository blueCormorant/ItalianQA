from flask import render_template, flash, redirect
from app import app
from app.forms import QAForm, LoginForm
from app.qa.qa import QuestionAnswerer
import psycopg2.pool
import os

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
        return render_template("index.html", title="Home", form=form, answer=answer)
    else:
        return render_template(
          "index.html",
          title="Home",
          form=form,
          default_question=answerer.default_question,
          default_context=answerer.default_context
        )

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for {form.username.data}")
    return render_template("login.html", title="Login", form=form)
