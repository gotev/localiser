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

import os
import time

from generators.common.interfaces \
    import SeparatedNamespacesGenerator, TranslationFunction, ProjectSupportingFilesArguments, \
    NamespaceSupportingFilesArguments
from generators.common import utils


class IosGenerator(SeparatedNamespacesGenerator):
    def _sanitize_namespace_name(self, name: str):
        filtered = utils.filter_chars_numbers(name)
        return filtered[:1].upper() + filtered[1:]

    def _sanitize_localised_key_value(self, value: str):
        return value.strip().replace('"', '\\"')

    def _get_supporting_files_dir(self, project_output_dir: str):
        outputDir = os.path.join(project_output_dir, 'Sources', 'LocaliserExtensions')
        utils.make_dir(outputDir)
        return outputDir

    def _get_translation_function_parameters(self, value: str):
        placeholders = utils.get_placeholders(value)

        if not placeholders:
            return ''

        return ', '.join('{}: CustomStringConvertible'.format(p.variableName) for p in placeholders)

    def name(self):
        return 'iOS'

    def get_package_name(self):
        return 'generators.ios'

    def get_base_output_directory_name(self):
        return 'ios'

    def get_localisation_directory_base_path(self, project_name: str, project_short_identifier: str):
        return os.path.join('Sources', 'Resources')

    def get_localisation_directory_name(self, slug: str, default_slug: str):
        if slug == default_slug:
            return 'Base.lproj'

        if '_' not in slug:
            return '{}.lproj'.format(slug)

        temp = slug.split('_', 1)

        return '{}-{}.lproj'.format(temp[0], temp[1].upper())

    def get_namespace_file_name(self, namespace: str):
        return '{}.strings'.format(self._sanitize_namespace_name(namespace))

    def get_namespace_template(self):
        return 'namespace.strings'

    def get_namespace_key_prefix(self, namespace: str):
        return ''

    def _copy_raw_file(self, environment, template_name: str, destination: str, executable=False):
        with open(destination, 'w') as file:
            template = environment.get_template(template_name)
            file.write(
                template.render()
            )

        if executable:
            utils.make_executable(destination)

    def generate_project_supporting_files(self, arguments: ProjectSupportingFilesArguments):
        outputDir = self._get_supporting_files_dir(arguments.project_output_dir)

        outputFile = os.path.join(outputDir, 'String+{}.swift'.format(arguments.project_short_identifier.capitalize()))

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('String+Project.swift')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier
                )
            )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='HTMLString.swift',
            destination=os.path.join(arguments.project_output_dir, 'Sources', 'HTMLString.swift'),
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gitignore',
            destination=os.path.join(arguments.project_output_dir, '.gitignore'),
        )

        outputFile = os.path.join(arguments.project_output_dir, 'Package.swift')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('Package.swift')
            file.write(
                template.render(
                    projectPackageName=arguments.project_name + "Strings"
                )
            )

        outputFile = os.path.join(arguments.project_output_dir, 'README.md')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('README.md')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectPackageName=arguments.project_name + "Strings",
                    projectShortIdentifier=arguments.project_short_identifier
                )
            )

        outputFile = os.path.join(arguments.project_output_dir, 'LICENSE')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('LICENSE')
            file.write(
                template.render(
                    projectOrganization=arguments.project_organization,
                    year=time.strftime("%Y")
                )
            )

    def generate_namespace_supporting_files(self, arguments: NamespaceSupportingFilesArguments):
        projectNamespace = self._sanitize_namespace_name(arguments.namespace_name)
        outputDir = self._get_supporting_files_dir(arguments.project_output_dir)
        outputFile = os.path.join(outputDir, 'String+{}{}.swift'.format(arguments.project_short_identifier.capitalize(),
                                                                        projectNamespace))

        translationFunctions = [
            TranslationFunction(
                name=utils.camelize(key['key']),
                localisedKey=key['key'].strip(),
                localisedKeyValue=self._sanitize_localised_key_value(key['value']),
                localisedKeyValueContainsHTML=key['contains_HTML'],
                localisedKeyComment=utils.to_comment_lines(key['comment']),
                parameters=self._get_translation_function_parameters(key['value']),
                placeholders=utils.get_placeholders(key['value'])
            )
            for key in arguments.localised_keys
        ]

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('String+Namespace.swift')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier,
                    projectNamespace=projectNamespace,
                    translationFunctions=translationFunctions
                )
            )
