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
from ..model import hep2oai_dc


@hep2oai_dc.over('identifier', '^(dois|persistent_identifiers)$')
def dois2marc(self, key, value):
    """Other Standard Identifier."""
    value = utils.force_list(value)

    def get_value(val):
        return {
            val.get('value')
        }

    self['identifier'] = self.get('identifier', [])
    for val in value:
        self['identifier'].append(get_value(val))
    return self['identifier']


@hep2oai_dc.over('creator', '^authors$')
def authors2marc(self, key, value):
    """Main Entry-Personal Name."""
    value = utils.force_list(value)

    def get_value(value):
        return {
            value.get('full_name'),
        }
    self["creator"] = self.get('creator', [])
    for author in value:
        self["creator"].append(get_value(author))
    return self["creator"]


# @hep2oai_dc.over('title', '^titles$')
# @utils.for_each_value
# @utils.filter_values
# def titles2marc(self, key, value):
#     """Title Statement."""
#     return {
#         value.get('title'),
#     }


# @hep2oai_dc.over('abstract', 'abstracts')
# @utils.for_each_value
# @utils.filter_values
# def abstract2marc(self, key, value):
#     """Summary, Etc.."""
#     value = utils.force_list(value)
#     def get_value(value):
#         return {
#             value.get('value')
#         }
#     self['abstract'] = self.get('abstract', [])
#     for abst in value:
#         self['abstract'].append(get_value(abst))
#     return self['abstract']

# TODO
# @hep2oai_dc.over('date', 'earliest_date')
# @utils.for_each_value
# @utils.filter_values
# def abstract2marc(self, key, value):
#     """Summary, Etc.."""
#     return {
#         value
#     }

# @hep2oai_dc.over('publisher', 'publication_info')
# @utils.for_each_value
# @utils.filter_values
# def publication_info2marc(self, key, value):
#     """Publication info about record."""
#     return {
#         '0': value.get('recid'),
#         'c': value.get('page_artid'),
#         'n': value.get('journal_issue'),
#         'o': value.get('conf_acronym'),
#         'p': value.get('journal_title'),
#         'r': value.get('reportnumber'),
#         't': value.get('confpaper_info'),
#         'v': value.get('journal_volume'),
#         'w': value.get('cnum'),
#         'x': value.get('pubinfo_freetext'),
#         'y': value.get('year'),
#         'z': value.get('isbn'),
#         'm': value.get('note')
#     }
