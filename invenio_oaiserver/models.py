# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAuth2Server is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from sqlalchemy import ForeignKey
from invenio_db import db
from sqlalchemy_utils import Timestamp

class Set(db.Model, Timestamp):
    """
    """

    __tablename__ = 'oaiset'

    spec = db.Column(
        db.String(40),
        primary_key=True,
        info=dict(
            label='Name',
            description='Name of set.'
        )
    )

    name = db.Column(
        db.String(40),
        info=dict(
            label='Long name',
            description='Long name of set.'
        )
    )
    """Human readable name of the set."""

    description = db.Column(
        db.Text(),
        default=u'',
        info=dict(
            label='Description',
            description='Optional. Description of the set',
        )
    )
    """Human readable description."""

    search_pattern = db.Column(
        db.Text(),
        default=u'',
        info=dict(
            label='Search pattern',
            description='Search pattern to select records',
        )
    )
    """Search pattern to get records."""

    search_index = db.Column(
        db.Text(),
        default=u'',
        info=dict(
            label='ElasticSearch index',
            description='Index to search in the ElasticSearch',
        )
    )

    search_doc_type = db.Column(
        db.Text(),
        default=u'',
        info=dict(
            label='ElasticSearch doc_type',
            description='Document type to look for in the ElasticSearch',
        )
    )
    # collection = db.Column(
    #     db.Integer(),
    #     default=-1,
    #     info=dict(
    #         label='Description',
    #         description='Optional. Description of the set',
    #     )
    # )
    # """Collection to provide via OAI-PMH."""

    parent_name = db.Column(db.Text(),
                            ForeignKey('oaiset.spec'),
                            default=None)


    parent = db.relationship(
        "Set",
        remote_side=[spec],
        backref="oaiset",
        cascade="all, delete-orphan",
        single_parent=True
    )

    def get_full_spec(self):
        if self.parent:
            return self.parent.get_full_spec()+":"+self.spec
        else:
            return self.spec


# class SetRecord(db.Model):
#     """
#     """

#     __tablename__ = 'oaisetrecord'

#     set_spec = db.Column(
#         db.Text(),
#         ForeignKey(Set.spec),
#         primary_key=True,
#         info=dict(
#             label='Set spec'
#         )
#     )
#     recid = db.Column(
#         db.Integer(),
#         primary_key=True,
#         info=dict(
#             label='Record id'
#         )
#     )
#     is_deleted = db.Column(
#         db.Boolean(),
#         default=False,
#         info=dict(
#             label="Deleted?",
#             description="Is record deleted from the set?"
#         )
#     )
#     create_date = db.Column(
#         db.DateTime(),
#         default=func.now(),
#         info=dict(
#             label='Creation date',
#             desciption='Date of record being added to the OAI set.'
#         )
#     )
#     last_modified = db.Column(
#         db.DateTime(),
#         onupdate=func.utc_timestamp(),
#         info=dict(
#             label='Last modified',
#             desciption='Last modification date.'
#         )
#     )

#     set = db.relationship(
#         "Set",
#         remote_side=[Set.spec],
#         backref="records"
#     )
