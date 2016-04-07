from flask import Flask, make_response, render_template, request
from pyformat import app
from pyformat.parser import PythonParser

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/format', methods=['POST'])
def format():
    prefix, ast = PythonParser.parse(request.form['source'] or '')
    return render_template('source.html', ast=ast, comment_prefix=prefix)

@app.route('/save', methods=['POST'])
def save():
    json = request.get_json()
    response = make_response()

    for key in request.cookies:
        response.set_cookie(key, '', expires=0)

    for name, color in json['colors'].items():
        response.set_cookie(name, color)
    for name in json['checked']:
        response.set_cookie(name, 'checked')
    for name in json['ignored']:
        response.set_cookie(name, 'ignore')

    return response
