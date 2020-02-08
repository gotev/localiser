"""
Localiser Generator
Copyright (C) 2019  Aleksandar Gotev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pathlib
import collections
import re
import os
import stat
import textwrap

LocaliserPlaceholder = collections.namedtuple('LocaliserPlaceholder', 'placeholder variableName')

placeholders_matcher = re.compile('\\${[A-Za-z]+}')
placeholder_translator = str.maketrans({'$': '', '{': '', '}': ''})

chars_filter = re.compile('[^a-zA-Z0-9 _]')


def filter_chars_numbers(string: str, keep_case=False):
    filtered = '_'.join(chars_filter.sub('', string).split())

    if not keep_case:
        filtered = filtered.lower()

    if filtered == '':
        raise Exception('Sorry, but you have to fix {} which does not contain a single valid ASCII character. '
                        'Cannot continue.'.format(string))

    return filtered


def camelize(string: str, keep_case=False):
    components = filter_chars_numbers(string, keep_case).split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def make_dir(directory: str):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def make_executable(file: str):
    st = os.stat(file)
    os.chmod(file, st.st_mode | stat.S_IEXEC)


def get_placeholders(string: str, escape_key_function=None):
    placeholders = re.findall(placeholders_matcher, string)

    def nothing(value):
        return value

    if not escape_key_function:
        escape_key_function = nothing

    return [LocaliserPlaceholder(placeholder=escape_key_function(placeholder),
                                 variableName=placeholder.translate(placeholder_translator).lower())
            for placeholder in placeholders]


def to_comment_lines(string: str, comment_begin_sequence='//'):
    if not string:
        return None

    polished = string.replace('\n', '').replace('\r', '')
    wrapped = textwrap.wrap(polished, 60)
    return ['{} {}'.format(comment_begin_sequence, line) for line in wrapped]
