OAISERVER_ADMIN_EMAIL = "someone@example.com"
OAISERVER_RESUMPTION_TOKEN_EXPIRE_TIME = 1  # time in hours
OAISERVER_SETS_MAX_LENGTH = 3

OAISERVER_METADATA_FORMATS = {
    "oai_dc": {
        "dojosn_file": "local/path",
        "schemaURL": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "namespaceURL": "http://www.openarchives.org/OAI/2.0/oai_dc/",
        "template": "local/path"
    }
}

OAISERVER_NAMESPACE_IDENTIFIER = "repo.example.com"
OAISERVER_SCHEMA_ORCID_PATH = "/pid/orcid"
OAISERVER_SCHEMA_SET_PATH = "/oai/sets"
