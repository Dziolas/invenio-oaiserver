# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAIServer is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""OAI-PMH 2.0 server."""

from celery import shared_task
from invenio_oaiserver.models import Set
from invenio_record.api import Record
from invenio_search import Query, current_search_client
from invenio_oaiserver.config import (OAISERVER_SCHEMA_ORCID_PATH,
                                      OAISERVER_SCHEMA_SET_PATH)
from datetime import datetime
from invenio_oaiserver.oaiid_provider import OaiIdProvider


@shared_task
def update():
    sets = Set.query.all()
    for set in sets:
        query = Query(form.query.data)
        response = current_search_client.search(
            index=set.search_index,
            doc_type=set.search_doc_type,
            body=query.body
        )
        ids = [(a['_id'], _get_oaiid(a)) for a in response['hits']['hits']]

        # get all current records with this set
        current_ids = []

        # new records that need to be added
        new_ids = ids - current_ids

        # records that were deleted from the set
        del_ids = current_ids - ids

        _add_records_to_set(new_ids, set.spec)
        _del_records_from_set(del_ids, set.spec)


def _add_records_to_set(ids, set_name):
    # use invenio-record functions to add set information to the record
    # get record via invenio-record.api.Record.... get_record
    for recid, oaiid in ids:
        if oaiid:
            rec = Record.get_record(recid)
            rec.patch(create_new_set_patch(set_name))
        else:
            #use minter for this
            oaiid = OaiIdProvider.create('rec',recid)
            rec = Record.get_record(recid)
            rec.patch(create_oaiid_patch(oaiid))
            rec.patch(create_new_set_patch(set_name))

def _del_records_from_set(ids, set_name):
    for recid, oaiid in ids:
        rec = Record.get_record(recid)
        old_datastamp = _get_oai_set_datastamp(rec)
        rec.patch(delete_set_patch(set_name, old_datastamp))


def _get_oaiid(record):
    path = OAISERVER_SCHEMA_ORCID_PATH.split('/')
    for p in path:
        if p in record:
            record = record[p]
        else:
            record = ''
            break
    return record

def _get_oai_set_datastamp(record):
    path = OAISERVER_SCHEMA_SET_PATH.split('/')
    for p in path:
        if p in record:
            record = record[p]
        else:
            record = ''
            break
    return record['datastamp']


def create_oaiid_patch(oaiid):
    return [
            {"op": "add",
             "path": OAISERVER_SCHEMA_ORCID_PATH,
             "value":oaiid}
           ]


def create_new_set_patch(set_name):
    return [
            {"op": "add",
             "path": OAISERVER_SCHEMA_SET_PATH,
             "value": {"id": set_name,
                       "datastamp":datetime.now(),
                       "status":""}}
            ]

def delete_set_patch(set_name, old_datastamp):
    # need to be changed to support multiple sets and do not overwrite everything
    return [
            {"op": "replace",
             "path": OAISERVER_SCHEMA_SET_PATH,
             "value": {"id": set_name,
                       "datastamp":old_datastamp,
                       "status":"deleted"}}
            ]
