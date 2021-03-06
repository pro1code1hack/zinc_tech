import logging
import sys

from flask import Flask
from flask_migrate import Migrate
import os
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from models.models import Ticket, Event     # It is essential to import the models here, otherwise the alembic will not be able to find them

basedir = os.path.abspath(os.path.dirname(__file__))




def create_app(db_location):
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection
    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("api.log"), logging.StreamHandler()],
    )
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'   # TODO: use .env file
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True


    from database import db

    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)


    #bcrypt = Bcrypt(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'z1nc'
        }
    )
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    api = Api(app)

    return app



if __name__ == '__main__':
    app = create_app("site.db")
    app.run(debug=False,  port=8070, host = "0.0.0.0")

