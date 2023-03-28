from flask import render_template, flash, redirect
from app import app
from app.forms import QAForm, LoginForm
from app.qa.qa import QuestionAnswerer

answerer = QuestionAnswerer()

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    form = QAForm()
    print(form.context)
    if form.validate_on_submit():
        answer = answerer.answer_question(
          form.context.data,
          form.question.data
        )
        return render_template(
          "index.html",
          title="Home",
          form=form,
          answer=answer
        )
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
keys = db.keys()
