from models.models import database
from models.models import Asset
import re


hex_pattern = re.compile(r'[0-9a-fA-F]{16}')


def report_asset_for_maintenance(unique_identifier: str) -> bool:
    """
    Sets the 'serviceRequired' flag on the asset to True. Asset is identified using the
    'uniqueIdentifier' value. This value must be
    :param unique_identifier:
    :return: True if succeeds, False otherwise
    """

    # verify 'unique_identifier' matches the pattern
    if not re.match(hex_pattern, unique_identifier):
        return False

    # ensure an asset exists in the database
    asset = database.session.query(Asset).filter(Asset.uniqueIdentifier == unique_identifier).scalar()
    if asset is not None:
        # set the 'serviceRequired' field for that asset to True
        database.session.query(Asset).filter(Asset.uniqueIdentifier == unique_identifier).\
            update({'serviceRequired': True}, synchronize_session=False)
        database.session.commit()
        database.session.flush()
        return True
    else:
        return False
