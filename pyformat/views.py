from flask import Flask, flash, make_response, redirect
from flask import render_template, request, url_for
from pyformat import app, db
from pyformat.models import Paste
from pyformat.parser import PythonParser

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/paste', methods=['POST'])
def paste():
    source = request.form['source']
    if source is None:
        flash("You can't submit an empty paste")
        return redirect(url_for('index'))
    try:
        PythonParser.parse(source)
    except SyntaxError:
        flash('Syntax error in source')
        return redirect(url_for('index'))
    new_paste = Paste(source)
    db.session.add(new_paste)
    db.session.commit()
    return redirect(url_for('view', paste_id=new_paste.id))

@app.route('/<int:paste_id>')
def view(paste_id):
    text = Paste.query.get_or_404(paste_id).text
    prefix, ast = PythonParser.parse(text)
    return render_template('source.html', ast=ast, comment_prefix=prefix)

@app.route('/save-settings', methods=['POST'])
def save_settings():
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
