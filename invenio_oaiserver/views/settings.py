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
from invenio_oaiserver.models import Set, SetRecord
from wtforms import Form, fields, validators, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from invenio_db import db
from flask import current_app as app


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
        # sets = [(set.name, set.name) for set in Set.query.all()]
        # sets.insert(0, (0, "No parent set"))

        spec = fields.StringField(
            'Set spec',
            validators=[validators.InputRequired()],
        )
        name = fields.StringField(
            'Set long name',
            validators=[validators.InputRequired()],
        )
        description = fields.StringField(
            'Description'
        )
        parent = QuerySelectField(
            query_factory=Set.query.all,
            get_pk=lambda a: a.spec,
            get_label=lambda a: a.name,
            allow_blank=True,
            blank_text='No parent set'
        )
        #     'Parent set',
        #     choices=sets,
        # )
        search_pattern = fields.StringField(
            'Query',
            validators=[validators.InputRequired()]  # query_or_collection_check]
        )
        # collection = fields.SelectMultipleField(
        #     'Collection',
        #     choices=[(-1,"No collection"),(1,"Tmp Collection 1"),(2,"Tmp Collection 2"),(3,"Tmp Collection 3")],
        # )
    return NewSetForm(*args, **kwargs)


# @app.before_request
# def before_request():
#     method = request.form.get('_method', '').upper()
#     if method:
#         request.environ['REQUEST_METHOD'] = method
#         ctx = flask._request_ctx_stack.top
#         ctx.url_adapter.default_method = method
#         assert request.method == method

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/sets')
def manage_sets():
    """Manage sets."""
    sets = Set.query.filter(Set.parent == None)
    return render_template('sets.html', sets=sets)


@blueprint.route('/sets/new')
def new_set():
    """Manage sets."""
    return render_template('make_set.html', new_set_form=get_NewSetForm())


@blueprint.route('/sets/edit/<spec>')
def edit_set(spec):
    """Manage sets."""
    set_to_edit = Set.query.filter(Set.spec==spec).one()
    return render_template('edit_set.html',
                           edit_set_form=get_NewSetForm(obj=set_to_edit))


@blueprint.route('/sets/new', methods=['POST'])
def submit_set():
    """Insert a new set."""
    form = get_NewSetForm(request.form)
    if request.method == 'POST' and form.validate():
        new_set = Set(spec=form.spec.data,
                      name=form.name.data,
                      description=form.description.data,
                      search_pattern=form.search_pattern.data,
                      #collection=form.collection.data,
                      parent=form.parent.data)
        db.session.add(new_set)

        # creating connetion with records
        # records = get_records(form.query.data)
        recids = [1,2,3]
        for recid in recids:
            new_set_record = SetRecord(set_spec=form.spec.data,
                                       recid=recid)
            db.session.add(new_set_record)

        db.session.commit()
        flash('New set was added.')
        return redirect(url_for('.manage_sets'))
    return render_template('make_set.html', new_set_form=form)


@blueprint.route('/sets/edit/<spec>', methods=['POST'])
def submit_edit_set(spec):
    """Insert a new set."""
    form = get_NewSetForm(request.form)
    if request.method == 'POST' and form.validate():
        print("I was eddited")
        # db.session.add(new_set)

        # # creating connetion with records
        # # records = get_records(form.query.data)
        # recids = [1,2,3]
        # for recid in recids:
        #     new_set_record = SetRecord(set_spec=form.spec.data,
        #                                recid=recid)
        #     db.session.add(new_set_record)

        # db.session.commit()
        flash('Set was changed')
        return redirect(url_for('.manage_sets'))
    return render_template('edit_set.html', edit_set_form=form, spec=spec)

# @blueprint.route('/set/<str:name>', methods=['DELETE'])
@blueprint.route('/sets/<spec>/delete')
def delete_set(spec):
    """Manage sets."""
    SetRecord.query.filter(SetRecord.set_spec==spec).delete()
    Set.query.filter(Set.spec==spec).delete()
    db.session.commit()
    flash('Set %s was deleted.' % spec)
    return redirect(url_for('.manage_sets'))
