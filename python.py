import ast
import json

class PythonToJson(ast.NodeVisitor):
    def visit_Module(self, node):
        return json.dumps([self.generic_visit(child) for child in node.body])

    def generic_visit(self, node):
        fields = dict()
        for fieldname, value in ast.iter_fields(node):
            if isinstance(value, list):
                fields[fieldname] = [self.generic_visit(x) for x in value]
            elif isinstance(value, ast.AST):
                fields[fieldname] = self.generic_visit(value)
            else:
                fields[fieldname] = value
        return { type(node).__name__: fields }

    @classmethod
    def parse(cls, source):
        '''Convert the string of Python source code into a JSON representation
of its AST.'''
        return cls().visit(ast.parse(source))

if __name__ == '__main__':
    print(PythonToJson.parse(source))
