from flask_sqlalchemy import SQLAlchemy
from secrets import token_hex


database = SQLAlchemy()


class Asset(database.Model):
    """ Asset Model for storing asset related details """
    __tablename__ = 'Assets'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    uniqueIdentifier = database.Column(database.String(16), nullable=False, default=token_hex(8))
    building = database.Column(database.String(255), nullable=False)
    roomNumber = database.Column(database.String(255), nullable=False)
    appliance = database.Column(database.String(255), nullable=False)
    serviceRequired = database.Column(database.Boolean, nullable=False, default=False)
    userID = database.Column(database.Integer, database.ForeignKey('Users.id'))

    def __repr__(self) -> str:
        return "<Asset(id={0}, uniqueIdentifier={1}, building={2}, roomNumber={3}, appliance={4}, " \
               "serviceRequired={5}, userID={6})>".format(
                    self.id,
                    self.uniqueIdentifier,
                    self.building,
                    self.roomNumber,
                    self.appliance,
                    self.serviceRequired,
                    self.user_id
                )


class User(database.Model):
    """ User Model for storing user related details """
    __tablename__ = 'Users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = database.Column(database.String(255), nullable=False, unique=True)
    passwordHash = database.Column(database.String(128), nullable=False)
    salt = database.Column(database.String(64), nullable=False)
    email = database.Column(database.String(255), nullable=False, unique=True)

    assets = database.relationship(Asset)

    def __repr__(self):
        return "<Task(id={0}, username={1}, passwordHash={2}, salt={3}, email={4}, assets={5})>".format(
            self.id,
            self.username,
            self.passwordHash,
            self.salt,
            self.email,
            self.assets
        )
