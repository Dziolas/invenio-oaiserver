from oaiid_provider import OaiIdProvider


def recid_minter(record_uuid, data):
    """Mint record identifiers."""
    #repalce control_number witha configurable path
    assert 'control_number' not in data
    provider = OaiIdProvider.create(
        object_type='rec', object_uuid=record_uuid)
    data['control_number'] = int(provider.pid.pid_value)
    return provider.pid
