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

from generators.android.generator import AndroidGenerator
from generators.ios.generator import IosGenerator
from generators.json.generator import JsonGenerator
from generators.common.database import LocaliseDatabase

import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('database_path', type=str, help='Path to the localiser SQLite database')
parser.add_argument('project_name', type=str, help='Name of the project you want to export')
parser.add_argument('project_version', type=str, help='Version of the exported project')
parser.add_argument('output_dir', nargs='?', type=str, default='./generated', help='Export output directory')

args = parser.parse_args()

print("""
Localiser Generator  Copyright (C) 2019  Aleksandar Gotev
This program comes with ABSOLUTELY NO WARRANTY; For details see LICENSE.
This is free software, and you are welcome to redistribute it
under certain conditions.
""")

projectVersion = args.project_version.strip()

db = LocaliseDatabase(args.database_path.strip())

# register generators here
generators = [AndroidGenerator(), IosGenerator(), JsonGenerator()]

project = db.get_project_by_name(args.project_name.strip())

if not project:
    print('No such project "{}"'.format(args.project_name.strip()))
    availableProjects = db.get_available_projects()

    if not availableProjects:
        print('No available projects in this database.')
    else:
        print('\nAvailable projects:')
        for row in availableProjects:
            print('- {}'.format(row['name']))

    sys.exit(1)

else:
    print('Exporting project "{}" (id {})'.format(project['name'], project['id']))

defaultLanguage = db.get_project_default_language(project['id'])

print('  Default localisation is {} (id {})'.format(defaultLanguage['slug'], defaultLanguage['id']))

projectNamespaces = db.get_project_namespaces(project['id'])

if not projectNamespaces:
    print('  Project must have at least one namespace')
    sys.exit(1)

print('  {} total namespaces'.format(len(projectNamespaces)))

for projectNamespace in projectNamespaces:
    print('    - {} (id {})'.format(projectNamespace['name'], projectNamespace['id']))

totalKeys = db.get_project_total_keys(project['id'])

if not totalKeys:
    print('  Project must have at least one localised key')
    sys.exit(1)

print('  {} total localised keys'.format(totalKeys[0]))

projectLanguages = db.get_project_languages(project['id'])

print('  {} total locales'.format(len(projectLanguages)))
print('Creating output directories')

for generator in generators:
    generator.run(args.output_dir.strip(), db, project, projectVersion, projectNamespaces, projectLanguages,
                  defaultLanguage)
