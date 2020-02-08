from unittest import TestCase
from generators.common import utils
from generators.common.utils import LocaliserPlaceholder


class TestUtils(TestCase):

    def test_filter_chars_numbers(self):
        self.assertEqual('12435923ciao', utils.filter_chars_numbers('12435923""ciao|!"£$%&/()=?'))

    def test_filter_chars_numbers_with_spaces_tabs(self):
        self.assertEqual('12_4359_23_ciao', utils.filter_chars_numbers('12 4359    23" "ciao  |!"£     $%&/()=?'))

    def test_filter_chars_numbers_keeping_case(self):
        self.assertEqual('12_4359_23_cIAo',
                         utils.filter_chars_numbers('12 4359    23" "cIAo  |!"£     $%&/()=?', keep_case=True))

    def test_filter_chars_numbers_with_underscores(self):
        self.assertEqual('something_which_must_be_the_same',
                         utils.filter_chars_numbers('something_which_must_be_the_same'))

    def test_filter_chars_error(self):
        self.assertRaises(Exception, utils.filter_chars_numbers, '!"£$%&/()=?)(/&%$£"')

    def test_camelize(self):
        self.assertEqual('testCaseOne', utils.camelize('test case one'))

    def test_camelize_2(self):
        self.assertEqual('testcaseone', utils.camelize('testCaseOne'))

    def test_camelize_3(self):
        self.assertEqual('testCaseOne', utils.camelize('testCaseOne', keep_case=True))

    def test_camelize_4(self):
        self.assertEqual('testCaseOne', utils.camelize('test_case_one'))

    def test_camelize_5(self):
        self.assertEqual('testCaseOne', utils.camelize('test_Case_One', keep_case=True))

    def test_no_placeholders(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all'))

    def test_invalid_placeholder(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all for ${}'))

    def test_invalid_placeholder_2(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all for $ {hello}'))

    def test_invalid_placeholder_3(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all for ${__123}'))

    def test_invalid_placeholder_4(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all for ${name45}'))

    def test_invalid_placeholder_5(self):
        self.assertEqual([], utils.get_placeholders('hi nothing at all for ${45name}'))

    def test_valid_placeholder(self):
        self.assertEqual([LocaliserPlaceholder(placeholder='${name}', variableName='name')],
                         utils.get_placeholders('hi nothing at all for ${name}'))

    def test_valid_placeholder_2(self):
        self.assertEqual([LocaliserPlaceholder(placeholder='${nAMe}', variableName='name')],
                         utils.get_placeholders('hi nothing at all for ${nAMe}'))

    def test_comment_lines_short(self):
        string = ' this is a line of regular comment'
        self.assertEqual(['// {}'.format(string)], utils.to_comment_lines(string))

    def test_comment_lines_long(self):
        string = ' this is a line of regular comment which is very long and spreads across more than a single line ' \
                 'so it should be split in multiple comment lines'
        self.assertEqual(['//  this is a line of regular comment which is very long and',
                          '// spreads across more than a single line so it should be split',
                          '// in multiple comment lines'],
                         utils.to_comment_lines(string))
