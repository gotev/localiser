"""
Localiser UI
Copyright (C) 2019  Aleksandar Gotev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.db import models
from simple_history.models import HistoricalRecords


class Locale(models.Model):
    slug = models.CharField(max_length=5,
                            help_text='<a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" target="_blank">'
                                      'ISO 639-1</a> or '
                                      '<a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2" target="_blank">'
                                      'ISO 3166-1</a> string. (e.g. it, en, fr, it-IT, en-US, ..)')
    history = HistoricalRecords()

    def __str__(self):
        return self.slug


class Project(models.Model):
    name = models.CharField(max_length=128,
                            help_text='The name of your app (e.g. My App)')
    organization = models.CharField(max_length=128,
                                    help_text='The name of the organization which owns this project (e.g. ACME Org)')
    package = models.CharField(max_length=128,
                               help_text='The package (or bundle identifier) which will be used in the '
                                         'auto-generated strings library (e.g. com.company.project.strings)')
    short_identifier = models.CharField(max_length=10,
                                        help_text='The identifier which will be used in the auto-generated '
                                                  'libraries as the root to get access to your localisation strings '
                                                  'from code. (e.g. iOS: Strings.shortidentifier.namespace.string(), '
                                                  'Android: ShortidentifierStrings.namespace.string(context) )')
    ios_deployment_target = models.CharField(max_length=10,
                                             default='11.4',
                                             help_text='The minimum iOS version you want to support (e.g. 11.4). '
                                                       'Android minimum is set to API 18 (Android 4.3)')

    android_min_sdk = models.IntegerField(default=18,
                                          help_text='Minimum Android SDK version to support (e.g. 18 - Android 4.3)')

    internal_maven_repo_url = models.CharField(max_length=1024,
                                               help_text='(optional) Internal maven repository URL to deploy the '
                                                         'library locally on a dev computer. '
                                                         'file:///Users/yourusername/workspace/maven-repo/releases)',
                                               null=True,
                                               blank=True)

    nexus_maven_repo_url = models.CharField(max_length=1024,
                                            help_text='(optional) Nexus (or Artifactory or other maven repo) maven '
                                                      'repository URL. '
                                                      '(e.g. https://maven.yourcompany.com/repository/your-library/)',
                                            null=True,
                                            blank=True)

    default_language = models.ForeignKey(Locale,
                                         on_delete=models.CASCADE,
                                         help_text='The base localisation of your project (e.g. en)')

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Namespace(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,
                            help_text='The namespace is a way to group your strings. It\'s up to you to decide if you '
                                      'want to group them by feature, section or whatever else (e.g. home)')
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'name'], name='unique_namespace')
        ]

    def __str__(self):
        return '{} - {}'.format(self.project, self.name)


class LocalisedKey(models.Model):
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    comment = models.TextField(null=True, blank=True,
                               help_text='Something useful to specify what this key is for and where to use it '
                                         '(e.g. This is the text shown to the user only the first time he enters the '
                                         'app. You have to use it only in welcome screen.)')
    contains_HTML = models.BooleanField(default=False,
                                        help_text="Indicates if this localisation key contains HTML in its values")
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['namespace', 'key'], name='unique_key_in_namespace')
        ]

    def __str__(self):
        return '{} - {} - {}'.format(self.namespace.project, self.namespace.name, self.key)


class TranslatedKey(models.Model):
    localised_key = models.ForeignKey(LocalisedKey, on_delete=models.CASCADE)
    slug = models.ForeignKey(Locale, on_delete=models.CASCADE)
    value = models.CharField(max_length=2048)
    temporary = models.BooleanField(default=False,
                                    help_text='To speed up development and have the possibility to better '
                                              'define a translation later, you can mark a translated key as '
                                              '"Temporary" and change its value later. There\'s a filter which '
                                              'helps you see only temporary strings')
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['localised_key', 'slug'], name='unique_translated_key')
        ]

    def __str__(self):
        return '{}'.format(self.value)
