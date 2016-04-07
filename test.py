import unittest
from unittest.mock import patch

class TestStringEndFinder(unittest.TestCase):
    def setUp(self):
        from pyformat.parser import CommentParser
        self.index_after_string = CommentParser.index_after_string

    def test_find_string_end(self):
        self.assertEqual(self.index_after_string("print('foo')", 6), 11)

    def test_unterminated_string(self):
        string = "print('foo)"
        self.assertEqual(self.index_after_string(string, 6), len(string))

    def test_invalid_start_index(self):
        self.assertRaises(ValueError, self.index_after_string, "'foo'", 1)

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

    def test_prefixes_comment(self, randint):
        self.assertEqual(self.tag_comments('# foo'), ('0', "'0# foo'\n"))

if __name__ == '__main__':
    unittest.main()
