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

from django.contrib import admin
from django.forms import TextInput
from simple_history.admin import SimpleHistoryAdmin

from database.models import *

name = 'Localiser'

admin.site.site_header = name
admin.site.site_title = name
admin.site.index_title = name


class InlineNamespace(admin.TabularInline):
    model = Namespace
    ordering = ('name',)
    show_change_link = True
    extra = 1


class InlineLocalisedKey(admin.TabularInline):
    model = LocalisedKey
    ordering = ('key',)
    show_change_link = True
    extra = 3


class InlineTranslatedKey(admin.TabularInline):
    model = TranslatedKey
    ordering = ('localised_key',)
    show_change_link = True
    extra = 3


class ProjectAdmin(SimpleHistoryAdmin):
    save_on_top = True
    ordering = ('name',)
    list_display = ('name', 'default_language', 'short_identifier', 'package', 'ios_deployment_target')
    search_fields = ['name', ]
    inlines = [
        InlineNamespace,
    ]


class NamespaceAdmin(SimpleHistoryAdmin):
    save_on_top = True
    ordering = ('project', 'name')
    list_display = ('name', 'project')
    list_filter = ('project',)
    search_fields = ['name', ]
    inlines = [
        InlineLocalisedKey,
    ]


class LocalisedKeyAdmin(SimpleHistoryAdmin):
    save_on_top = True
    ordering = ('key',)
    list_display = ('key', 'namespace')
    list_filter = ('namespace', 'contains_HTML')
    search_fields = ['key', ]
    inlines = [
        InlineTranslatedKey,
    ]


class TranslatedKeyAdmin(SimpleHistoryAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }
    # save_on_top = True # disabled because of https://github.com/treyhunner/django-simple-history/issues/443
    list_display = ('value', 'slug', 'localised_key', 'temporary')
    search_fields = ['value', ]
    list_filter = ('slug', 'localised_key__namespace__project', 'localised_key__namespace', 'temporary')


admin.site.register(Locale, SimpleHistoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(LocalisedKey, LocalisedKeyAdmin)
admin.site.register(TranslatedKey, TranslatedKeyAdmin)
