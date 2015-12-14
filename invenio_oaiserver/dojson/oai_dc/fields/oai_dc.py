# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""OAI DublinCore model definition."""

from dojson import utils
from ..model import hep2marc


@hep2marc.over('024', '^(dois|persistent_identifiers)$')
def dois2marc(self, key, value):
    """Other Standard Identifier."""
    value = utils.force_list(value)

    def get_value(val):
        return {
            'a': val.get('value'),
            '9': val.get('source'),
            '2': val.get('type') or "DOI"
        }

    self['024'] = self.get('024', [])
    for val in value:
        self['024'].append(get_value(val))
    return self['024']


@hep2marc.over('035', 'external_system_numbers')
@utils.for_each_value
@utils.filter_values
def external_system_numbers2marc(self, key, value):
    """System Control Number."""
    return {
        'a': value.get('value'),
        '9': value.get('institute'),
        'z': value.get('obsolete'),
    }


@hep2marc.over('100', '^authors$')
def authors2marc(self, key, value):
    """Main Entry-Personal Name."""
    value = utils.force_list(value)

    def get_value(value):
        affiliations = [
            aff.get('value') for aff in value.get('affiliations', [])
        ]
        return {
            'a': value.get('full_name'),
            'e': value.get('role'),
            'q': value.get('alternative_name'),
            'i': value.get('inspire_id'),
            'j': value.get('orcid'),
            'm': value.get('email'),
            'u': affiliations,
            'x': value.get('recid'),
            'y': value.get('claimed')
        }

    if len(value) > 1:
        self["700"] = []
    for author in value[1:]:
        self["700"].append(get_value(author))
    return get_value(value[0])

@hep2marc.over('210', '^title_variation$')
@utils.for_each_value
@utils.filter_values
def title_variation2marc(self, key, value):
    """Title variation."""
    return {
        'a': value,
    }


@hep2marc.over('245', '^titles$')
@utils.for_each_value
@utils.filter_values
def titles2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('title'),
        'b': value.get('subtitle'),
        '9': value.get('source'),
    }

@hep2marc.over('520', 'abstracts')
@utils.for_each_value
@utils.filter_values
def abstract2marc(self, key, value):
    """Summary, Etc.."""
    return {
        'a': value.get('value'),
        '9': value.get('source'),
    }

@hep2marc.over('773', 'publication_info')
@utils.for_each_value
@utils.filter_values
def publication_info2marc(self, key, value):
    """Publication info about record."""
    return {
        '0': value.get('recid'),
        'c': value.get('page_artid'),
        'n': value.get('journal_issue'),
        'o': value.get('conf_acronym'),
        'p': value.get('journal_title'),
        'r': value.get('reportnumber'),
        't': value.get('confpaper_info'),
        'v': value.get('journal_volume'),
        'w': value.get('cnum'),
        'x': value.get('pubinfo_freetext'),
        'y': value.get('year'),
        'z': value.get('isbn'),
        'm': value.get('note')
    }
