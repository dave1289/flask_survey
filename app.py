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
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions')
def first_question():
    options = []
    for opt in satisfaction_survey.questions[question_index].choices:
        options.append(opt)
    return render_template('questions.html', options=options, question=question_set[question_index])


@app.route('/questions/answer')
def record_answers():
    global question_index
    options = []
    question_index += 1
    if question_index < len(question_set):
        for opt in satisfaction_survey.questions[question_index].choices:
            options.append(opt)
        prev_answer = request.args.getlist('answers')
        survey_responses.extend(prev_answer)
    else:
        question_index = 0
        user_answer = request.args.getlist('answers')
        survey_responses.extend(user_answer)
        return render_template('thank_you.html', answers=survey_responses, questions=question_set)

    return render_template('questions.html', question=question_set[question_index], options=options)

@app.route('/return-home')
def return_home():
    global question_index
    global survey_responses
    question_index = 0
    survey_responses = []
    return render_template('home.html', survey=satisfaction_survey)




