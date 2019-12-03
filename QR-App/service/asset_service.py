from models.models import User
from models.models import database, Asset

"""
This module is responsible for basic CRUD operations with the database.
Authentication is not handled in this module nor is data sanitation (at the moment).
"""


def get_user_assets(username: str) -> [Asset]:
    """
    Returns all the assets belonging to the user given the username.

    :param username: username of user
    :return: a list of Assets
    """
    user_id = database.session.query(User.id).filter(User.username == username).scalar()
    return database.session.query(Asset).filter(Asset.userID == user_id).all()


def get_specific_user_asset(username: str, asset_id: int) -> Asset:
    """
    Returns an asset given the username and asset_id.

    :param username: username of user
    :param asset_id: id of the asset
    :return: Asset object if exists or None otherwise
    """
    user_id = database.session.query(User.id).filter(User.username == username).scalar()
    asset: Asset = database.session.query(Asset).filter(
        Asset.userID == user_id,
        Asset.id == asset_id
    ).scalar()

    if asset is not None:
        return asset
    else:
        return None


def update_specific_asset(username: str, asset_id: int, asset: Asset) -> int:
    """
    Updates an assets which already exists belonging to a specific user. This function
    returns a 0 if the asset was successfully updated.

    :param username: username of user
    :param asset_id: id of asset
    :param asset: an asset object containing the changed values. these values
                  include: appliance, building, roomNumber, and serviceRequired
                  all other values are disregarded
    :return: 0 - success
    """
    user_id: int = database.session.query(User.id).filter(User.username == username).scalar()
    database.session.query(Asset).filter(
        Asset.userID == user_id,
        Asset.id == asset_id
    ).update(
        {
            'appliance': asset.appliance,
            'building': asset.building,
            'roomNumber': asset.roomNumber,
            'serviceRequired': asset.serviceRequired
        },
        synchronize_session=False
    )
    database.session.commit()
    return 0


def remove_specific_asset(username: str, asset_id) -> int:
    """
    Removes a specific asset which exists to a specific user. This function returns
    a 0 value is the asset was successfully deleted from the database.

    :param username: username of user
    :param asset_id: id of asset
    :return: 0 - success
    """
    user_id: int = database.session.query(User.id).filter(User.username == username).scalar()
    database.session.query(Asset).filter(
        Asset.userID == user_id,
        Asset.id == asset_id
    ).delete()
    database.session.commit()
    return 0


def create_asset(username: str, asset: Asset) -> int:
    """
    Creates an asset for the user. Returns 0 upon successful creation and database update.

    :param username:username of user
    :param asset: an asset object containing set attributes. these values
                  include: appliance, building, roomNumber, and serviceRequired
                  all other attributes belonging to this object are overwritten or
                  set to default values for security
    :return: 0 - success
    """
    user_id: int = database.session.query(User.id).filter(User.username == username).scalar()
    asset.userID = user_id
    asset.id = None
    asset.uniqueIdentifier = None
    database.session.add(asset)
    database.session.commit()
    return 0
