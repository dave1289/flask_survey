from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from string import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SLAP'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
