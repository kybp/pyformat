import unittest
from unittest.mock import patch

class TestStringEndFinder(unittest.TestCase):
    def setUp(self):
        from pyformat.parser import CommentParser
        self.index_after_string = CommentParser.index_after_string

    def test_find_string_end(self):
        self.assertEqual(self.index_after_string("print('foo')", 6), 11)

    def test_handles_double_quotes(self):
        self.assertEqual(self.index_after_string('"foo"', 0), 5)

    def test_unterminated_string(self):
        string = "print('foo)"
        self.assertEqual(self.index_after_string(string, 6), len(string))

    def test_invalid_start_index(self):
        self.assertRaises(ValueError, self.index_after_string, "'foo'", 1)

    def test_handles_long_string(self):
        self.assertEqual(self.index_after_string("'''a\nb'''", 0), 9)

@patch('random.randint', return_value=0)
class TestPrefixGenerator(unittest.TestCase):
    def setUp(self):
        from pyformat.parser import CommentParser
        self.get_safe_prefix = CommentParser.get_safe_prefix

    def test_gets_prefix(self, randint):
        self.assertEqual(self.get_safe_prefix(''), '0')

    def test_gets_unused_prefix(self, randint):
        self.assertEqual(self.get_safe_prefix('"0"'), '00')

@patch('random.randint', return_value=0)
class TestCommentParser(unittest.TestCase):
    def setUp(self):
        from pyformat.parser import CommentParser
        self.tag_comments = CommentParser.tag_comments

    def test_echoes_non_comment(self, randint):
        self.assertEqual(self.tag_comments('pass'), ('0', 'pass'))

    def test_echoes_strings(self, randint):
        self.assertEqual(self.tag_comments('"foo"'), ('0', '"foo"'))

    def test_prefixes_comment(self, randint):
        self.assertEqual(self.tag_comments('# foo'), ('0', "'0# foo'"))

    def test_does_not_add_superfluous_newlines(self, randint):
        _, out = self.tag_comments('# foo\n# bar\n')
        self.assertEqual(out.count('\n'), 2)

    def test_puts_eol_comment_on_preceding_line(self, randint):
        self.assertEqual(self.tag_comments('pass # foo'),
                         ('0', "'0# foo'\npass"))

    def test_properly_indents_comment(self, randint):
        self.assertEqual(self.tag_comments('if True:\n  pass # foo'),
                         ('0', "if True:\n  '0# foo'\n  pass"))

    def test_escapes_quotes_in_comment(self, randint):
        self.assertEqual(self.tag_comments("#'foo'"), ('0', r"'0#\'foo\''"))

    def test_escapes_backslashes_in_comments(self, randint):
        self.assertEqual(self.tag_comments("#\\foo\\"),
                         ('0', r"'0#\\foo\\'"))

    def test_discards_carriage_return(self, randint):
        self.assertEqual(self.tag_comments('pass\r\npass'),
                         ('0', 'pass\npass'))

if __name__ == '__main__':
    unittest.main()
