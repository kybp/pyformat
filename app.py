import ast
from flask import Flask, make_response, render_template, request

class PythonParser(ast.NodeVisitor):
    def visit_Module(self, node):
        return [self.generic_visit(child) for child in node.body]

    def generic_visit(self, node):
        fields = { 'node_type': type(node).__name__ }
        for fieldname, value in ast.iter_fields(node):
            if isinstance(value, list):
                fields[fieldname] = [self.generic_visit(x) for x in value]
            elif isinstance(value, ast.AST):
                fields[fieldname] = self.generic_visit(value)
            else:
                fields[fieldname] = value
        return fields

    @classmethod
    def parse(cls, source):
        return cls().visit(ast.parse(source))

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

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/format', methods=['POST'])
def format():
    ast = PythonParser.parse(request.form['source'] or '')
    return render_template('source.html', ast=ast)

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

if __name__ == '__main__':
    app.run(debug=True)
