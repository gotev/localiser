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

from abc import ABCMeta, abstractmethod
import collections
import os
import jinja2
from generators.common import utils

TranslationFunction = collections.namedtuple('TranslationFunction',
                                             'localisedKey '
                                             'localisedKeyValue '
                                             'localisedKeyValueContainsHTML '
                                             'localisedKeyComment '
                                             'name '
                                             'parameters '
                                             'placeholders')

ProjectSupportingFilesArguments = collections.namedtuple('ProjectSupportingFilesArguments',
                                                         'project_name '
                                                         'project_organization '
                                                         'project_language '
                                                         'project_short_identifier '
                                                         'project_package '
                                                         'project_version '
                                                         'project_namespaces '
                                                         'project_ios_deployment_target '
                                                         'project_android_min_sdk '
                                                         'project_internal_maven_repo '
                                                         'project_nexus_maven_repo '
                                                         'project_output_dir '
                                                         'environment')

NamespaceSupportingFilesArguments = collections.namedtuple('NamespaceSupportingFilesArguments',
                                                           'project_name '
                                                           'project_short_identifier '
                                                           'project_package '
                                                           'project_version '
                                                           'namespace_name '
                                                           'localised_keys '
                                                           'project_output_dir '
                                                           'environment')


class ILocaliserGenerator:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def run(self, output_dir, db, project, project_version, project_namespaces, project_languages, default_language):
        raise NotImplementedError


class SeparatedNamespacesGenerator(ILocaliserGenerator):
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    def run(self, output_dir, db, project, project_version, project_namespaces, project_languages, default_language):
        print('  Creating {} output directory'.format(self.name()))
        generator_output_path = os.path.join(output_dir, self.get_base_output_directory_name())
        generator_environment = jinja2.Environment(loader=jinja2.PackageLoader(self.get_package_name()))
        # https://stackoverflow.com/a/35777386
        generator_environment.trim_blocks = True
        generator_environment.lstrip_blocks = True

        utils.make_dir(generator_output_path)

        print('  Creating {} supporting files'.format(self.name()))

        available_namespaces = []

        for project_namespace in project_namespaces:
            localised_keys = db.get_namespace_localised_keys(project_namespace['id'], default_language['id'])

            if localised_keys:
                available_namespaces.append(project_namespace['name'])
                self.generate_namespace_supporting_files(
                    NamespaceSupportingFilesArguments(
                        project_name=project['name'],
                        project_short_identifier=project['short_identifier'],
                        project_package=project['package'],
                        project_version=project_version,
                        namespace_name=project_namespace['name'],
                        localised_keys=localised_keys,
                        project_output_dir=generator_output_path,
                        environment=generator_environment
                    )
                )

        self.generate_project_supporting_files(
            ProjectSupportingFilesArguments(
                project_name=project['name'],
                project_language=default_language['slug'],
                project_organization=project['organization'],
                project_short_identifier=project['short_identifier'],
                project_package=project['package'].strip(),
                project_version=project_version,
                project_namespaces=available_namespaces,
                project_android_min_sdk=project['android_min_sdk'],
                project_internal_maven_repo=project['internal_maven_repo_url'],
                project_nexus_maven_repo=project['nexus_maven_repo_url'],
                project_ios_deployment_target=project['ios_deployment_target'].strip(),
                project_output_dir=generator_output_path,
                environment=generator_environment
            )
        )

        localisation_base_path = os.path.join(
            generator_output_path,
            self.get_localisation_directory_base_path(project['name'], project['short_identifier']))
        utils.make_dir(localisation_base_path)

        for projectLanguage in project_languages:
            language_directory_name = self.get_localisation_directory_name(
                slug=projectLanguage['slug'].strip().lower(),
                default_slug=default_language['slug'].strip().lower()
            )

            print('    Creating {}'.format(language_directory_name))
            language_directory = os.path.join(localisation_base_path, language_directory_name)
            utils.make_dir(language_directory)

            for project_namespace in project_namespaces:
                translated_keys = db.get_translated_keys(project_namespace['id'], projectLanguage['id'])
                count_translated_keys = len(translated_keys)

                skip_text = ''

                if count_translated_keys == 0:
                    skip_text = ', skipping it'

                print('      Found {} keys for namespace {} with locale {}{}'.format(
                    len(translated_keys),
                    project_namespace['name'],
                    projectLanguage['slug'],
                    skip_text)
                )

                if count_translated_keys > 0:
                    output_file_name = self.get_namespace_file_name(project_namespace['name'])

                    with open(os.path.join(language_directory, output_file_name), 'w') as namespaceFile:
                        template = generator_environment.get_template(self.get_namespace_template())
                        namespaceFile.write(
                            template.render(
                                keyPrefix=self.get_namespace_key_prefix(project_namespace['name']),
                                translatedKeys=translated_keys
                            )
                        )

    def name(self): raise NotImplementedError

    @abstractmethod
    def get_package_name(self): raise NotImplementedError

    @abstractmethod
    def get_base_output_directory_name(self): raise NotImplementedError

    @abstractmethod
    def get_localisation_directory_base_path(self,
                                             project_name: str,
                                             project_short_identifier: str): raise NotImplementedError

    @abstractmethod
    def get_localisation_directory_name(self, slug: str, default_slug: str): raise NotImplementedError

    @abstractmethod
    def get_namespace_file_name(self, namespace: str): raise NotImplementedError

    @abstractmethod
    def get_namespace_template(self): raise NotImplementedError

    @abstractmethod
    def get_namespace_key_prefix(self, namespace: str): raise NotImplementedError

    @abstractmethod
    def generate_project_supporting_files(self, arguments: ProjectSupportingFilesArguments): raise NotImplementedError

    @abstractmethod
    def generate_namespace_supporting_files(self,
                                            arguments: NamespaceSupportingFilesArguments): raise NotImplementedError
