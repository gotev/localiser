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
import base64
import time

from generators.common.interfaces \
    import SeparatedNamespacesGenerator, TranslationFunction, ProjectSupportingFilesArguments, \
    NamespaceSupportingFilesArguments
from generators.common import utils


class AndroidGenerator(SeparatedNamespacesGenerator):
    def _get_module_name(self, project_name: str):
        return '{}-strings'.format(project_name.lower().replace('_', '-'))

    def _get_source_supporting_files_dir(self,
                                         project_name: str, project_output_dir: str, project_package: str):
        subDirs = project_package.split('.')
        outputDir = os.path.join(project_output_dir,
                                 self._get_module_name(project_name), 'src', 'main', 'java', *subDirs)
        utils.make_dir(outputDir)
        return outputDir

    def _sanitize_namespace(self, namespace: str):
        return utils.filter_chars_numbers(namespace)

    def _get_translation_function_parameters(self, value: str):
        placeholders = utils.get_placeholders(value)

        if not placeholders:
            return ''

        return ', '.join('{}: String'.format(p.variableName) for p in placeholders)

    def _sanitize_localised_key(self, namespace: str, key: str):
        return self.get_namespace_key_prefix(namespace) + key.strip().replace(' ', '_').replace('-', '_')

    def _escape_key(self, key):
        return key.strip().replace('$', '\\$')

    def name(self):
        return 'Android'

    def get_package_name(self):
        return 'generators.android'

    def get_base_output_directory_name(self):
        return 'android'

    def get_localisation_directory_base_path(self, project_name: str, project_short_identifier: str):
        return os.path.join(self._get_module_name(project_name), 'src', 'main', 'res')

    def get_localisation_directory_name(self, slug: str, default_slug: str):
        if slug == default_slug:
            return 'values'

        if '_' not in slug:
            return 'values-{}'.format(slug)

        temp = slug.split('_', 1)

        return 'values-{}-r{}'.format(temp[0], temp[1].upper())

    def get_namespace_file_name(self, namespace: str):
        return '{}.xml'.format(self._sanitize_namespace(namespace))

    def get_namespace_template(self):
        return 'namespace.xml'

    def get_namespace_key_prefix(self, namespace: str):
        return '{}_'.format(self._sanitize_namespace(namespace))

    def _copy_raw_file(self, environment, template_name: str, destination: str, executable=False):
        with open(destination, 'w') as file:
            template = environment.get_template(template_name)
            file.write(
                template.render()
            )

        if executable:
            utils.make_executable(destination)

    def generate_project_supporting_files(self, arguments: ProjectSupportingFilesArguments):
        outputDir = self._get_source_supporting_files_dir(arguments.project_name,
                                                          arguments.project_output_dir,
                                                          arguments.project_package)
        moduleOutputDir = os.path.join(arguments.project_output_dir,
                                       self._get_module_name(arguments.project_name))

        moduleMainOutputDir = os.path.join(moduleOutputDir, 'src', 'main')
        projectGroup = '.'.join(arguments.project_package.split('.')[:2])
        moduleName = self._get_module_name(arguments.project_name)

        outputFile = os.path.join(outputDir, '{}Strings.kt'.format(arguments.project_short_identifier.capitalize()))

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('Project.kt')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier,
                    projectPackage=arguments.project_package,
                    projectNamespaces=[self._sanitize_namespace(n) for n in arguments.project_namespaces]
                )
            )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/gitignore',
            destination=os.path.join(arguments.project_output_dir, '.gitignore'),
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/gradlew',
            destination=os.path.join(arguments.project_output_dir, 'gradlew'),
            executable=True
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/gradlew.bat',
            destination=os.path.join(arguments.project_output_dir, 'gradlew.bat'),
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/gradle.properties',
            destination=os.path.join(arguments.project_output_dir, 'gradle.properties'),
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/build.gradle',
            destination=os.path.join(arguments.project_output_dir, 'build.gradle'),
        )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/module/proguard-rules.pro',
            destination=os.path.join(moduleOutputDir, 'proguard-rules.pro'),
        )

        wrapperOutDir = os.path.join(arguments.project_output_dir, 'gradle', 'wrapper')
        utils.make_dir(wrapperOutDir)

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/wrapper/gradle-wrapper.properties',
            destination=os.path.join(wrapperOutDir, 'gradle-wrapper.properties'),
        )

        # This is absolute madness. No way of getting a gradle-wrapper.jar from an URL.
        # So in order to generate a fully functional project, a cached one in base64 must be used.
        with open(os.path.join(wrapperOutDir, 'gradle-wrapper.jar'), 'wb') as file:
            template = arguments.environment.get_template('gradle/wrapper/gradle-wrapper.jar.b64')
            base64data = template.render()
            file.write(base64.b64decode(base64data))

        outputFile = os.path.join(arguments.project_output_dir, 'manifest.gradle')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('gradle/manifest.gradle')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier,
                    projectVersion=arguments.project_version,
                    projectOrganization=arguments.project_organization,
                    projectInternalMavenRepo=arguments.project_internal_maven_repo,
                    projectNexusMavenRepo=arguments.project_nexus_maven_repo,
                    projectAndroidMinSdk=arguments.project_android_min_sdk,
                    projectGroup=projectGroup,
                    moduleName=moduleName
                )
            )

        outputFile = os.path.join(arguments.project_output_dir, 'README.md')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('README.md')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier,
                    projectInternalMavenRepo=arguments.project_internal_maven_repo,
                    projectNexusMavenRepo=arguments.project_nexus_maven_repo,
                    projectVersion=arguments.project_version,
                    projectGroup=projectGroup,
                    moduleName=moduleName
                )
            )

        outputFile = os.path.join(moduleMainOutputDir, 'AndroidManifest.xml')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('gradle/module/AndroidManifest.xml')
            file.write(
                template.render(
                    projectPackage=arguments.project_package
                )
            )

        self._copy_raw_file(
            environment=arguments.environment,
            template_name='gradle/module/build.gradle',
            destination=os.path.join(moduleOutputDir, 'build.gradle'),
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

        outputFile = os.path.join(arguments.project_output_dir, 'settings.gradle')

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('gradle/settings.gradle')
            file.write(
                template.render(
                    libraryModule=self._get_module_name(arguments.project_name)
                )
            )

    def generate_namespace_supporting_files(self, arguments: NamespaceSupportingFilesArguments):
        projectNamespace = self._sanitize_namespace(arguments.namespace_name)
        outputDir = self._get_source_supporting_files_dir(arguments.project_name,
                                                          arguments.project_output_dir,
                                                          arguments.project_package)
        outputFile = os.path.join(outputDir,
                                  '{}{}Strings.kt'.format(arguments.project_short_identifier.capitalize(),
                                                          projectNamespace.capitalize()))

        translationFunctions = [
            TranslationFunction(
                name=utils.camelize(key['key']),
                localisedKey=self._sanitize_localised_key(arguments.namespace_name, key['key']),
                localisedKeyValue=key['value'],
                localisedKeyValueContainsHTML=key['contains_HTML'],
                localisedKeyComment=utils.to_comment_lines(key['comment']),
                parameters=self._get_translation_function_parameters(key['value']),
                placeholders=utils.get_placeholders(key['value'], self._escape_key)
            )
            for key in arguments.localised_keys
        ]

        with open(outputFile, 'w') as file:
            template = arguments.environment.get_template('Namespace.kt')
            file.write(
                template.render(
                    projectName=arguments.project_name,
                    projectShortIdentifier=arguments.project_short_identifier,
                    projectPackage=arguments.project_package,
                    projectNamespace=projectNamespace,
                    translationFunctions=translationFunctions
                )
            )
