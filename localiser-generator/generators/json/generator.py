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
from generators.common.interfaces import ILocaliserGenerator
from generators.common import utils
import os
import json


class JsonGenerator(ILocaliserGenerator):
    def run(self, output_dir, db, project, project_version, project_namespaces, project_languages, default_language):
        json_dir = os.path.join(output_dir, 'json')
        print('  Creating json output directory')
        utils.make_dir(json_dir)

        for language in project_languages:
            language_file = os.path.join(json_dir, '{}.json'.format(language['slug'].strip().lower()))

            language_namespaces = {}

            for project_namespace in project_namespaces:
                translated_keys = db.get_translated_keys(project_namespace['id'], language['id'])
                count_translated_keys = len(translated_keys)

                skip_text = ''

                if count_translated_keys == 0:
                    skip_text = ', skipping it'

                print('      Found {} keys for namespace {} with locale {}{}'.format(
                    len(translated_keys),
                    project_namespace['name'],
                    language['slug'],
                    skip_text)
                )

                if count_translated_keys > 0:
                    current_namespace = {}
                    for translated_key in translated_keys:
                        value = translated_key['value'].strip()
                        placeholders = utils.get_placeholders(translated_key['value'])

                        # Replace placeholders format from ${name} to {{name}}
                        if placeholders:
                            for placeholder in placeholders:
                                value = value.replace(placeholder.placeholder, '{{' + placeholder.variableName + '}}')

                        current_namespace[utils.filter_chars_numbers(translated_key['key'])] = value
                    language_namespaces[utils.filter_chars_numbers(project_namespace['name'])] = current_namespace

            with open(language_file, 'w') as json_file:
                json.dump(language_namespaces, json_file)
