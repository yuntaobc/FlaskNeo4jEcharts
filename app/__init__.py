from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from .models import Neo4jSession

bootstrap = Bootstrap()
moment = Moment()
neo4j_db = Neo4jSession()


def create_app(config_name):
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    neo4j_db.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='')

    return app
