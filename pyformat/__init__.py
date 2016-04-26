import os
import logging
import re
import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

def escape_quotes_filter(string):
    return re.sub("'", "\\'", string)
app.jinja_env.filters['escape_quotes'] = escape_quotes_filter

def op_name_filter(op_name):
    return {
        'Add': '+',
        'Sub': '-',
        'Mult': '*',
        'Div': '/',
        'FloorDiv': '//',
        'Mod': '%',
        'Eq': '==',
        'Lt': '<',
        'Gt': '>',
        'LtE': '<=',
        'GtE': '>='
    }[op_name]
app.jinja_env.filters['op_name'] = op_name_filter

import pyformat.views
