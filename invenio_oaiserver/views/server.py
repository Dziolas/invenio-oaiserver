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
                   request,
                   render_template,
                   g,
                   make_response)
from datetime import datetime

blueprint = Blueprint(
    'oai2d',
    __name__,
    url_prefix='/oai2d',
    static_folder="../static",
    template_folder="../templates/invenio_oaiserver/server/"
)


@blueprint.route('/', methods=['GET', 'POST'])
def server():
    from flask import current_app as app
    from invenio_oaiserver.views.verbs import (identify,
                                             list_sets,
                                             list_metadata_formats,
                                             list_records,
                                             list_identifiers,
                                             get_record)
    ALLOWED_VERBS = {'Identify': identify,
                     'ListSets': list_sets,
                     'ListMetadataFormats': list_metadata_formats,
                     'ListRecords': list_records,
                     'ListIdentifiers': list_identifiers,
                     'GetRecord': get_record}

    verb = request.args.get("verb")
    g.response_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%Sz")
    # g.admin_email = app.config['CFG_ADMIN_EMAIL']
    g.repository_name = app.config['THEME_SITENAME']
    # g.base_url = app.config['CFG_SITE_URL']+"/oai2d"
    g.base_url = "/oai2d"
    output_xml = None

    try:
        selected_verb = ALLOWED_VERBS[verb]
    except KeyError:
        g.error = {}
        g.error['message'] = "This is not a valid OAI-PMH verb: \
                              {0}".format(verb)
        g.error['type'] = "badValue"
        output_xml = render_template("error.xml")

    if not output_xml:
        output_xml = selected_verb()
    response = make_response(output_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# @blueprint.route('/error', methods=['GET', 'POST'])
# def show_error():
#     g.error = {}
#     g.error['message'] = "This is not a valid OAI-PMH verb: \
#                           {0}".format("none")
#     g.error['type'] = "badValue"
#     return render_template("error.xml")
