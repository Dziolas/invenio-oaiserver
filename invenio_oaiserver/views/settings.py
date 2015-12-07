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
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for)
from invenio_oaiserver.models import Set
from wtforms import Form, fields, validators, ValidationError
from invenio_db import db


blueprint = Blueprint(
    'oaisettings',
    __name__,
    url_prefix='/oaisettings',
    static_folder="../static",
    template_folder="../templates/invenio_oaiserver/settings/",
)


def get_NewSetForm(*args, **kwargs):
    def query_or_collection_check(form, field):
        if field and form.collection:
            raise ValidationError('There can be only one field given from: query, collection')

    class NewSetForm(Form):
        sets = [(set.name, set.name) for set in Set.query.all()]
        sets.insert(0, (0, "No parent set"))

        name = fields.StringField(
            'Set name',
            validators=[validators.InputRequired()],
        )
        description = fields.StringField(
            'Description',
            validators=[validators.InputRequired()],
        )
        parent = fields.SelectField(
            'Parent set',
            choices=sets,
        )
        query = fields.StringField(
            'Query',
            validators=[query_or_collection_check]
        )
        collection = fields.SelectField(
            'Collection',
            choices=[(-1,"No collection"),(1,"Tmp Collection 1"),(2,"Tmp Collection 2"),(3,"Tmp Collection 3")],
        )
        # XXX See nodes in models.py
        # consider_deleted_records = fields.BooleanField(
        #     'Consider deleted records',
        # )
        # force_run_on_unmodified_records = fields.BooleanField(
        #     'Force run on unmodified records',
        # )
        # filter_pattern = fields.StringField(
        #     'Search pattern',
        # )
        # filter_records = fields.StringField(
        #     'Record IDs',
        # )
        # schedule = fields.StringField(
        #     'Schedule',
        # )
        # requested_action = fields.SelectField(
        #     'Requested action',
        #     choices=[
        #         ('submit_save',) * 2,
        #         ('submit_run_and_schedule',) * 2,
        #         ('submit_schedule',) * 2,
        #         ('submit_run',) * 2,
        #     ]
        # )
        # confirm_hash_on_commit = fields.BooleanField(
        #     'Ensure record hash did not change during execution',
        # )
        # allow_chunking = fields.BooleanField(
        #     'Allow chunking this task to multiple workers',
        #     default=True,
        # )
        # The ones below this line are hidden by javascript later. Using
        # HiddenField here would make us lose validation in them. Perhaps a
        # better way to do this is to use a custom field, but I do not wish to
        # potentially compromise validation right now.
        # schedule_enabled = fields.BooleanField(
        #     'Run this rule periodically',
        # )
        # modify = fields.BooleanField(
        #     'Request modification instead of creation',
        # )
        # original_name = fields.StringField(
        #     'Original name for modification',
        # )

        # def validate_filter_records(self, field):
        #     """Ensure that `filter_records` can be parsed by intbitset."""
        #     if not field.data:
        #         field.data = intbitset(trailing_bits=True)
        #     else:
        #         try:
        #             field.data = ids_from_input(field.data)
        #         except TypeError:
        #             etype, evalue, etb = sys.exc_info()
        #             six.reraise(ValidationError, evalue, etb)

        # def validate_schedule(self, field):
        #     """Ensure that `schedule` is accepted by `croniter`."""
        #     if not field.data:
        #         return
        #     try:
        #         croniter(field.data)
        #     except Exception:
        #         # May be TypeError/KeyError/AttributeError, who knows what else
        #         # Let's play it safe.
        #         six.reraise(ValidationError, *sys.exc_info()[1:])

    return NewSetForm(*args, **kwargs)

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/sets')
def manage_sets():
    """Manage sets."""
    sets = Set.query.all()
    return render_template('sets.html', sets=sets)

@blueprint.route('/sets/new')
def new_set():
    """Manage sets."""
    return render_template('make_set.html', new_set_form=get_NewSetForm())


@blueprint.route('/sets/new', methods=['POST'])
def submit_set():
    """Insert or modify an existing set."""
    form = get_NewSetForm(request.form)
    if request.method == 'POST' and form.validate():
        new_set = Set(name=form.name.data,
                      description=form.description.data,
                      search_pattern=form.query.data,
                      collection=form.collection.data,
                      parent=form.parent.data)
        db.session.add(new_set)
        db.session.commit()
        flash('New set was added.')
        return redirect(url_for('.manage_sets'))
    return render_template('make_set.html', new_set_form=form)
