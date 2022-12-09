from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from string import *
from survey import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SLAP'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

question_set = []

question_index = 0

survey_responses = []

satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])
for question in satisfaction_survey.questions:
    question_set.append(question.question)

@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/questions/0')
def first_question():
    return render_template('questions.html', question=question_set[0])


@app.route('/questions/answer')
def record_answers():
    question_index += 1
    prev_answer = request.args['survey_answer']
    survey_responses.append(prev_answer)
    return render_template('questions.html', question=question_set[question_index])
    



