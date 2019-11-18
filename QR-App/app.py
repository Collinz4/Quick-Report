from flask import Flask
from models.models import database
from controller.report_controller import report_blueprint
import configuration


# configure flask application settings
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = configuration.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = configuration.SQLALCHEMY_DATABASE_URI
app.host = configuration.host
app.port = configuration.port
app.debug = configuration.debug

# initialize database relational mapper
database.init_app(app)

# register blueprints
app.register_blueprint(report_blueprint)


if __name__ == '__main__':
    app.run()
