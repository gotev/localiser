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

import sqlite3
import os
from generators.common import utils


class LocaliseDatabase:

    def __init__(self, database_path: str):
        if not os.path.exists(database_path):
            raise FileNotFoundError('Provided database does not exist at path: {}'.format(os.path.abspath(database_path)))

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row

        self._db = connection.cursor()

    def get_project_by_name(self, name: str):
        self._db.execute("""
            SELECT *
            FROM database_project 
            WHERE name LIKE ?
            """, (name,))
        data = self._db.fetchone()

        if data:
            project = dict(zip([c[0] for c in self._db.description], data))
            project['name'] = utils.filter_chars_numbers(project['name'], keep_case=True)
            project['short_identifier'] = utils.filter_chars_numbers(project['short_identifier'], keep_case=True)
            return project

        return data

    def get_available_projects(self):
        self._db.execute('SELECT name FROM database_project')
        return self._db.fetchall()

    def get_project_default_language(self, project_id: int):
        self._db.execute("""
            SELECT database_locale.id, database_locale.slug
            FROM database_locale
            JOIN database_project ON database_locale.id = database_project.default_language_id
            WHERE database_project.id = ?
            """, (project_id,))

        return self._db.fetchone()

    def get_project_namespaces(self, project_id: int):
        self._db.execute("""
            SELECT id, name
            FROM database_namespace
            WHERE project_id = ?
            ORDER BY name
            """, (project_id,))

        return self._db.fetchall()

    def get_namespace_localised_keys(self, namespace_id: int, locale_id: int):
        self._db.execute("""
            SELECT key, database_translatedkey.value, contains_HTML, comment
            FROM database_localisedkey
            JOIN database_translatedkey ON database_translatedkey.localised_key_id = database_localisedkey.id
            WHERE database_localisedkey.namespace_id = ? AND database_translatedkey.slug_id = ?
            ORDER BY key
            """, (namespace_id, locale_id))

        return self._db.fetchall()

    def get_project_total_keys(self, project_id: int):
        self._db.execute("""
            SELECT COUNT(database_localisedkey.id)
            FROM database_namespace
            JOIN database_localisedkey ON database_localisedkey.namespace_id = database_namespace.id
            WHERE database_namespace.project_id =  ?
            """, (project_id,))

        return self._db.fetchone()

    # get all locales for which at least one localisation key has been defined
    def get_project_languages(self, project_id: int):
        self._db.execute("""
            SELECT DISTINCT database_locale.id, database_locale.slug
            FROM database_project
            JOIN database_namespace ON database_namespace.project_id = database_project.id
            JOIN database_localisedkey ON database_localisedkey.namespace_id = database_namespace.id
            JOIN database_translatedkey ON database_translatedkey.localised_key_id = database_localisedkey.id
            JOIN database_locale ON database_locale.id = database_translatedkey.slug_id
            WHERE database_project.id = ?
            """, (project_id,))

        return self._db.fetchall()

    def get_translated_keys(self, namespace_id: int, language_id: int):
        self._db.execute("""
            SELECT database_localisedkey.key, database_translatedkey.value
            FROM database_translatedkey
            JOIN database_localisedkey ON database_translatedkey.localised_key_id = database_localisedkey.id
            JOIN database_namespace ON database_localisedkey.namespace_id = database_namespace.id
            WHERE database_namespace.id = ? AND database_translatedkey.slug_id = ?
            ORDER BY database_localisedkey.key
            """, (namespace_id, language_id))

        return self._db.fetchall()
