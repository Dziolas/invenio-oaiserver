# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAIServer is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from __future__ import absolute_import
from unittest import TestCase
from flask import g, Flask
from invenio_oaiserver.sets import get_sets_count
from invenio_oaiserver.ext import InvenioOAIServer
from datetime import (timedelta, datetime)
import re


class FlaskTestCase(TestCase):

    """Mix-in class for creating the Flask application"""

    def setUp(self):
        self.app = Flask('testapp')
        self.ext = InvenioOAIServer()
        assert 'invenio-oaiserver' not in self.app.extensions
        self.ext.init_app(self.app)
        assert 'invenio-oaiserver' in self.app.extensions

        self.oai_url = "localhost/oai2d"
        self.app.config.setdefault("THEME_SITENAME","Invenio")


    def tearDown(self):
        pass


class TestVerbs(FlaskTestCase):

    """Tests OAI-PMH verbs"""

    # def test_init():
    #     """Test extension initialization."""
    #     app = Flask('testapp')
    #     ext = InvenioOAIServer(app)
    #     assert 'invenio-oaiserver' in app.extensions

    #     app = Flask('testapp')
    #     ext = InvenioOAIServer()
    #     assert 'invenio-oaiserver' not in app.extensions
    #     ext.init_app(app)
    #     assert 'invenio-oaiserver' in app.extensions

    def test_no_verb(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <error code="badValue">This is not a valid OAI-PMH verb:None</error>
</OAI-PMH>""".format(response_date)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_wrong_verb(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Aaa', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <error code="badValue">This is not a valid OAI-PMH verb:Aaa</error>
</OAI-PMH>""".format(response_date)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_identify(self):
        ########
        # TODO: remove EARLIEST DATESTAMP placeholder
        ########
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Identify', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{date}</responseDate>
    <request verb="Identify">{url}</request>
    <Identify>
        <repositoryName>{repo_name}</repositoryName>
        <baseURL>{url}</baseURL>
        <protocolVersion>2.0</protocolVersion>
        <adminEmail>{admin_email}</adminEmail>
        <earliestDatestamp>1990-02-01T12:00:00Z</earliestDatestamp>
        <deletedRecord>transient</deletedRecord>
        <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
        <compression>deflate</compression>
     </Identify>
</OAI-PMH>""".format(date=response_date,
                     url=self.oai_url,
                     repo_name="localhost",  # self.app.config['CFG_SITE_NAME'],
                     admin_email=self.app.config['OAISERVER_ADMIN_EMAIL'])
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_identify_with_additional_args(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Identify&notAValidArg=True',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <request verb="Identify" notAValidArg="True">{1}</request>
    <error code="badArgument">
        You have passed too many arguments together withEXLUSIVE argument.
    </error>
</OAI-PMH>""".format(response_date, self.oai_url)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets(self):
        with self.app.test_client() as c:
            self.app.config['CFG_SETS_MAX_LENGTH'] = 10
            result = c.get('/oai2d?verb=ListSets',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <requestverb="ListSets">{1}</request>
    <ListSets>
        <set>
            <setSpec>music</setSpec>
            <setName>Music collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>This is a collection of wide range of music.</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(chopin)</setSpec>
            <setName>Chopin collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>Collection of music composed by Chopin</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(techno)</setSpec>
            <setName>Techno music collection</setName>
        </set>
        <set>
            <setSpec>pictures</setSpec>
            <setName>Pictures collection</setName>
        </set>
    </ListSets>
</OAI-PMH>""".format(response_date, self.oai_url)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets_long(self):
        with self.app.test_client() as c:
            self.app.config['OAISERVER_SETS_MAX_LENGTH'] = 3
            result = c.get('/oai2d?verb=ListSets',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            exp_date = datetime.strptime(response_date,"%Y-%m-%dT%H:%M:%Sz") + \
                timedelta(hours=self.app.config['OAISERVER_RESUMPTION_TOKEN_EXPIRE_TIME'])
            coursor = self.app.config['OAISERVER_SETS_MAX_LENGTH']
            list_size = get_sets_count()
            # TODO: remove placeholder value
            token = "xxx45abttyz"
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{date}</responseDate>
    <requestverb="ListSets">{url}</request>
    <ListSets>
        <set>
            <setSpec>music</setSpec>
            <setName>Music collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>This is a collection of wide range of music.</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(chopin)</setSpec>
            <setName>Chopin collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>Collection of music composed by Chopin</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(techno)</setSpec>
            <setName>Techno music collection</setName>
        </set>
        <resumptionToken expirationDate="{exp_date}" completeListSize="{list_size}" cursor="{coursor}">{token}</resumptionToken>
    </ListSets>
</OAI-PMH>""".format(date=response_date,
                     url=self.oai_url,
                     exp_date=exp_date,
                     list_size=list_size,
                     coursor=coursor,
                     token=token)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets_with_resumption_token(self):
        pass

    def test_list_sets_with_second_resumption_token(self):
        pass

    def test_list_sets_with_resumption_token_and_other_args(self):
        pass
