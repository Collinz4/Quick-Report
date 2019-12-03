from models.models import database
from models.models import Asset
import re

"""
Responsible for handling service calls from un-authenticated users (reporters).
Data sanitation is a main priority along with minimum input values used.
"""

hex_pattern = re.compile(r'[0-9a-fA-F]{16}')


def report_asset_for_maintenance(unique_identifier: str) -> bool:
    """
    Sets the 'serviceRequired' flag on the asset to True. Asset is identified using the
    'uniqueIdentifier' value which is 16 digits and hexadecimal.

    :param unique_identifier: 16 digit hexadecimal value
    :return: True - succeeds
             False - fails due to bad uniqueIdentifier value or non-existing asset
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
        return True
    else:
        return False
