from models.models import User
from models.models import database
import hashlib
import os
import binascii

"""
This module is primarily used for the creation and authentication of users.
"""


def create_new_user(username: str, plaintext_password: str, email: str) -> int:
    """
    Creates a new user and returns 0 if successful. This function checks for duplicate user names
    and emails in the database.

    :param username: username for new user (duplicates not allowed)
    :param plaintext_password: password will be hashed in this function
    :param email: email for new user (duplicated not allowed)
    :return: 0 - success
             1 - failed due to duplicate username
             2 - failed due to duplicate email
    """

    # check to see if a duplicate username exists
    if database.session.query(User).filter(User.username == username).scalar() is not None:
        return 1

    # check to see if a duplicate email exists
    if database.session.query(User).filter(User.email == email).scalar() is not None:
        return 2

    # salt and hash the password
    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    hashed_password: str = hashlib.pbkdf2_hmac(
        hash_name='sha512',
        password=plaintext_password.encode('utf-8'),
        salt=salt,
        iterations=10000
    )
    hashed_password = binascii.hexlify(hashed_password)

    # create a user object and persist to the database
    new_user: User = User(
        username=username,
        passwordHash=hashed_password,
        salt=salt,
        email=email
    )
    database.session.add(new_user)
    database.session.commit()
    return 0


def authenticate_existing_user(username: str, password_to_challenge: str) -> int:
    """
    Authenticates user using the username and password values. Will return a 0, 1, or 2
    based on the outcome of the authentication status.

    :param username: user's username
    :param password_to_challenge: user's claimed password
    :return: 0 - success
             1 - user doesn't exist for that username
             2 - user exists but password is incorrect
    """
    user: User = database.session.query(User).filter(User.username == username).scalar()

    # user doesn't exist
    if user is None:
        return 1

    # hash user password with user's salt value
    hashed_password_to_challenge = hashlib.pbkdf2_hmac(
        hash_name='sha512',
        password=password_to_challenge.encode(),
        salt=user.salt.encode(),
        iterations=10000
    )
    hashed_password_to_challenge = binascii.hexlify(hashed_password_to_challenge).decode()

    if hashed_password_to_challenge == user.passwordHash:
        return 0
    else:
        return 2
