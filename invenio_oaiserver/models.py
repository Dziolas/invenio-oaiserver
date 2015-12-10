# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAuth2Server is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey
from invenio_db import db

class Set(db.Model):
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


class SetRecord(db.Model):
    set_spec = db.Column(
        db.Text(),
        info=dict(
            label='Description',
            description='Optional. Description of the set',
        )
    )
    recid
    is_deleted
