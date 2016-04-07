import ast
import random
import re

class CommentParser(ast.NodeVisitor):
    def visit_Module(self, node):
        self.strings = set()
        self.generic_visit(node)
        return list(self.strings)

    def visit_Str(self, node):
        self.strings.add(node.s)

    @classmethod
    def get_safe_prefix(cls, source):
        '''Return a randomly generated string which no string in the source
begins with.'''
        strings = cls().visit(ast.parse(source))
        prefix = str(random.randint(0, 9))
        for i in range(len(strings)):
            while any(s.startswith(prefix) for s in strings[:i + 1]):
                prefix += str(random.randint(0, 9))
        return prefix

    @classmethod
    def index_after_string(cls, source, i):
        '''Return an index into source just past the end of a string. i should
point to the beginning of the opening delimiter of the string. If the
string is unterminated, return len(source).'''
        def end_of_long_string(i):
            return i + 2 < len(source) and source[i:i + 3] == end * 3 and\
                source[i - 1] != '\\'
        end = source[i]
        if end != '"' and end != "'":
            raise ValueError('index does not point to beginning of string ')
        long_string = False
        if i + 2 < len(source) and source[i:i + 3] == end * 3:
            long_string = True
            i += 3
        else:
            i += 1
        while i < len(source):
            if long_string and end_of_long_string(i):
                return i + 3
            elif source[i] == end and source[i - 1] != '\\':
                return i + 1
            else:
                i += 1
        return len(source)

    @classmethod
    def tag_comments(cls, source):
        '''Replace comments with prefixed strings. The prefix is randomly
generated so as not to conflict with any real strings in the
source. Returns a tuple of the prefix and a string containing the
prefixed comment-strings.'''
        prefix = cls.get_safe_prefix(source)
        output = ''
        line   = ''
        i      = 0
        while i < len(source):
            if source[i] == '"' or source[i] == "'":
                j = index_after_string(source, i)
                while i < j:
                    line += source[i]
                    i += 1
            elif source[i] == '#':
                output += re.match(r'\s*', line).group() + "'{}".format(prefix)
                while i < len(source) and source[i] != '\n':
                    if source[i] == "'" or source[i] == '\\':
                        output += '\\'
                    output += source[i]
                    i += 1
                if line == '':
                    output += "'"
                else:
                    output += "'\n"
            elif source[i] == '\n':
                output += line.rstrip() + '\n'
                line = ''
                i += 1
            else:
                line += source[i]
                i += 1
        return (prefix, output + line.rstrip())

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
