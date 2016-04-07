import ast

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
