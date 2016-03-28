import ast
from flask import Flask, render_template, request

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

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/format', methods=['POST'])
def format():
    ast = PythonParser.parse(request.form['source'] or '')
    return render_template('source.html', ast=ast)

if __name__ == '__main__':
    app.run(debug=True)
