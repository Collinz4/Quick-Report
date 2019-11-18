from flask_sqlalchemy import SQLAlchemy
from secrets import token_hex

database = SQLAlchemy()


class Asset(database.Model):
    """ Asset Model for storing asset related details """
    __tablename__ = 'Assets'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    uniqueIdentifier = database.Column(database.String(16), nullable=False, default=token_hex(16))
    building = database.Column(database.String(255), nullable=False)
    roomNumber = database.Column(database.String(255), nullable=False)
    appliance = database.Column(database.String(255), nullable=False)
    serviceRequired = database.Column(database.Boolean, nullable=False, default=False)
    userID = database.Column(database.Integer, database.ForeignKey('Users.id'))

    def __repr__(self) -> str:
        return "<Asset(id={0}, building={1}, roomNumber={2}, appliance={3}, serviceRequired={4}, user_id={5})>"\
                .format(self.id, self.building, self.roomNumber, self.appliance, self.serviceRequired, self.user_id)


class User(database.Model):
    """ User Model for storing user related details """
    __tablename__ = 'Users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = database.Column(database.String(255), nullable=False, unique=True)
    passwordHash = database.Column(database.String(128), nullable=False)
    email = database.Column(database.String(255), nullable=False, unique=True)

    assets = database.relationship(Asset)

    def __repr__(self):
        return "<Task(id={0}, username={1}, email={3}, assets={4})>"\
               .format(self.id, self.username, self.email, self.assets)
