# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAuth2Server is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from sqlalchemy.orm import validates
from invenio_db import db

# class Set(db.Model):
#     """
#     """

#     __tablename__ = 'oaiset'

#     name = db.Column(
#         db.String(40),
#         primary_key=True,
#         info=dict(
#             label='Name',
#             description='Name of set.'
#         )
#     )
#     """Human readable name of the set."""

#     description = db.Column(
#         db.Text(),
#         default=u'',
#         info=dict(
#             label='Description',
#             description='Optional. Description of the set',
#         )
#     )
#     """Human readable description."""

#     search_pattern = db.Column(
#         db.Text(),
#         default=u'',
#         info=dict(
#             label='Description',
#             description='Optional. Description of the set',
#         )
#     )
#     """Search pattern to get records."""

#     collection = db.Column(
#         db.Text(),
#         default=u'',
#         info=dict(
#             label='Description',
#             description='Optional. Description of the set',
#         )
#     )
#     """Collection to provide via OAI-PMH."""

#     # @validates('name')
#     # def validate_name(self, key, name):
#     #     """Validate name.
#     #     Name should not contain '/'-character. Root collection's name should
#     #     equal CFG_SITE_NAME. Non-root collections should not have name equal to
#     #     CFG_SITE_NAME.
#     #     """
#     #     if '/' in name:
#     #         raise ValueError("collection name shouldn't contain '/'-character")

#     #     if not self.is_root and name == cfg['CFG_SITE_NAME']:
#     #         raise ValueError(("only root collection can "
#     #                           "be named equal to the site's name"))

#     #     if self.is_root and name != cfg['CFG_SITE_NAME']:
#     #         warn('root collection name should be equal to the site name')

#     #     return name
