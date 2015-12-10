# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAIServer is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Sets helper functions."""

from flask import current_app as app
from invenio_oaiserver.models import Set


# TODO: to be removed and substituted with database
# SETS = [{'spec': 'music',
#          'name': 'Music collection',
#          'description': 'This is a collection of wide range of music.'},
#         {'spec': 'music:(chopin)',
#          'name': 'Chopin collection',
#          'description': 'Collection of music composed by Chopin'},
#         {'spec': 'music:(techno)',
#          'name': 'Techno music collection'},
#         {'spec': 'pictures',
#          'name': 'Pictures collection'}
#         ]


def get_sets_list(starting_position=0, max_length=None):
    if not max_length:
        max_length = app.config['OAISERVER_SETS_MAX_LENGTH']

    sets = Set.query.offset(starting_position)
    if max_length:
        sets.limit(max_length)
    return sets

    # TODO: in batabase implementation this should not get all elements
    #return SETS[starting_position:starting_position+max_length]


def get_sets_count():
    return Set.query.count()
