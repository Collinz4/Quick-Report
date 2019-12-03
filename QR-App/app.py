from flask import Flask
from models.models import database
from controller.report_blueprint import report_blueprint
from controller.default_blueprint import default_blueprint
from controller.asset_blueprint import asset_blueprint
import configuration
import os


# configure flask application settings
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = configuration.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = configuration.SQLALCHEMY_DATABASE_URI
app.host = configuration.host
app.port = configuration.port
app.debug = configuration.debug
app.secret_key = os.urandom(24)

# initialize database relational mapper
database.init_app(app)

# register blueprints
app.register_blueprint(report_blueprint)
app.register_blueprint(default_blueprint)
app.register_blueprint(asset_blueprint)


if __name__ == '__main__':
    app.run()
