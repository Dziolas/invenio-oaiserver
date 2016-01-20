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

from invenio_search import Query, current_search_client
from invenio_oaiserver.oaiid_provider import OaiIdProvider


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

        #this shoul be moved to UPDATER (celery task) and it sould always take care of adding records to sets.
        ##########
        query = Query(form.query.data)
        response = current_search_client.search(
            index="records",# make configurable PER SET
            doc_type="record",# make configurable PER SET
            body=query.body,
            fields="_id, oaiid" #path to oaiid as a configurable
        )
        ids = [(a['_id'], a['oaiid']) for a in response['hits']['hits']]
        add_records_to_set(ids)
        #########

        db.session.commit()
        flash('New set was added.')
        return redirect(url_for('.manage_sets'))
    return render_template('make_set.html', new_set_form=form)


@blueprint.route('/sets/edit/<spec>', methods=['POST'])
def submit_edit_set(spec):
    """Insert a new set."""
    form = get_NewSetForm(request.form)
    if request.method == 'POST' and form.validate():
        old_set = Set.query.filter(spec=spec)
        query = Query(old_set.search_pattern)
        old_recid = current_search_client.search(
            index="records",
            doc_type="record",
            body=query.body,
            fields="_id, oaiid"
        )
        query = Query(form.search_pattern)
        new_recid = current_search_client.search(
            index="records",
            doc_type="record",
            body=query.body,
            fields="_id, oaiid"
        )
        recids_to_delete = set(old_recid)-set(new_recid)
        # TODO: marks records as deleted from set
        remove_recids_from_set(recids_to_delete)
        add_records_to_set(new_recid)
        flash('Set was changed')
        return redirect(url_for('.manage_sets'))
    return render_template('edit_set.html', edit_set_form=form, spec=spec)

def add_records_to_set(ids):
    # use invenio-record functions to add set information to the record
    # get record via invenio-record.api.Record.... get_record
    for recid, oaiid in ids:
        if oaiid:
            #how to get and modify record
            rec = get_record(recid)
            rec.append('oai-set-name'=new_set.name)
        else:
            #use minter for this
            oaiid = OaiIdProvider.create('rec',recid)
            rec = get_record(recid)
            #append set nam to the record (with append date as a separete field)
            #this needs to be configurable
            rec.append('oai-set-name'=new_set.name)
        # new_set_record = SetRecord(set_spec=form.spec.data,
        #                            recid=recid)
        # db.session.add(new_set_record)

# @blueprint.route('/set/<str:name>', methods=['DELETE'])
# TODO: what happens when we delete a set
@blueprint.route('/sets/<spec>/delete')
def delete_set(spec):
    """Manage sets."""
    SetRecord.query.filter(SetRecord.set_spec==spec).delete()
    Set.query.filter(Set.spec==spec).delete()
    db.session.commit()
    flash('Set %s was deleted.' % spec)
    return redirect(url_for('.manage_sets'))
