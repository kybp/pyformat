from flask import Flask

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

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

import formatter.views
