from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from string import *
from survey import *

"""
This app takes a survey object with title, instructions, and questions to create a dynamic interface to create and display the questions while saving responses for the thank you page to display

Survey can have any amount of questions, answers per question, and will be adding text input functionality for **if allow_text:** and create text input for further information

Please reach out with any issues at davemcelhaney@gmail.com
"""

app = Flask(__name__)

app.config['SECRET_KEY'] = '089LKJa$#t2x9sgse2'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

question_set = []
# empty list for questions to index through

question_index = 0
# int for moving through question_set list

survey_responses = []
# empty list for answers to survey

# survey for app is created below, will add survey upload when we go over that functionality
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


# creates question_set from survey.questions
for question in satisfaction_survey.questions:
    question_set.append(question.question)

@app.route('/')
def show_home():
    # displays home page 
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions')
def first_question():
    #displays first question and begins the survey
    options = []
    for opt in satisfaction_survey.questions[question_index].choices:
        options.append(opt)
    return render_template('questions.html', options=options, question=question_set[question_index], num=question_index)


@app.route('/questions/answer')
def record_answers():
    # accepts previous answer and appends it to survey_responses and proceeds to next question or thankyou page
    global question_index
    options = []
    question_index += 1
    if question_index < len(question_set):
        for opt in satisfaction_survey.questions[question_index].choices:
            options.append(opt)
        prev_answer = request.args.getlist('answers')
        survey_responses.extend(prev_answer)
    else:
        # make thank you page save responses, index, and answers in session storage so we can pick up our survey at a later time
        question_index = 0
        user_answer = request.args.getlist('answers')
        survey_responses.extend(user_answer)
        return render_template('thank_you.html', answers=survey_responses, questions=question_set)

    return render_template('questions.html', question=question_set[question_index], options=options, num=question_index)

@app.route('/return-home')
def return_home():
    # returns home from end of survey or reset button on each page
    # sets question_index and survey_responses to their starting values
    global question_index
    global survey_responses
    question_index = 0
    survey_responses = []
    return render_template('home.html', survey=satisfaction_survey)




