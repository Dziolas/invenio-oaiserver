# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAIServer is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""OAI-PMH 2.0 server."""

from __future__ import absolute_import
from flask import (Blueprint,
                   render_template)
#from invenio_oaiserver.models import Set

blueprint = Blueprint(
    'oaisettings',
    __name__,
    url_prefix='/oaisettings',
    static_folder="../static",
    #template_folder="templates",
)


@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/sets')
def manage_sets():
    """Manage sets."""
    #sets = Set.query.all()

    #return dict(sets=sets)
    return
