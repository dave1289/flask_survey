from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from string import *
from survey import satisfaction_survey, personality_quiz

"""
This app takes a survey object with title, instructions, and questions to create a dynamic interface to create and display the questions while saving responses for the thank you page to display

Survey can have any amount of questions, answers per question, and will be adding text input functionality for **if allow_text:** and create text input for further information

Please reach out with any issues at davemcelhaney@gmail.com
"""

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

debug = DebugToolbarExtension(app)

question_set = []
# empty list for questions to index through

question_index = 0
# int for moving through question_set list

survey_responses = []
# empty list for answers to survey

# creates question_set from survey.questions
for question in satisfaction_survey.questions:
    question_set.append(question.question)

@app.route('/old-home')
def old_home_redirect():
    # redirect from old homepage
    return redirect('/')

@app.route('/')
def show_home():
    # displays home page 
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions')
def first_question():
    global question_index
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
    if 'answers' not in request.args:
        flash('Please choose a response', 'error')
        if question_index < len(question_set):
            for opt in satisfaction_survey.questions[question_index].choices:
                options.append(opt)
    else:
        question_index += 1
        if question_index < len(question_set):
            for opt in satisfaction_survey.questions[question_index].choices:
                options.append(opt)
            prev_answer = request.args.getlist('answers')
            survey_responses.extend(prev_answer)
        else:
            # make thank you page save responses, index, and answers in session storage so we can pick up our survey at a later time
            user_answer = request.args.getlist('answers')
            survey_responses.extend(user_answer)
            session['answers'] = survey_responses
            return render_template('thank_you.html', answers=survey_responses, questions=question_set)
    return render_template('questions.html', question=question_set[question_index], options=options, num=question_index)

@app.route('/return-home')
def return_home():
    # returns home from end of survey or reset button on each page
    # sets question_index and survey_responses to their starting values
    global question_index
    global survey_responses
    session['answers'] = []
    question_index = 0
    survey_responses = []
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/about-us')
def show_info():
    return render_template('about_us.html')

##**************************sessions demo**********************************
# @app.route('/login-form')
# def show_login():
#     return render_template('login_form.html')


# @app.route('/invitation')
# def show_invite():
#     if session.get('entered-pin', False):
#         return render_template('invite.html')
#     else:
#         return redirect('/login-form')

# @app.route('/login')
# def verify_secret_code():
#     session['entered-pin'] = request.args['secret_code']
#     return redirect('/invitation')