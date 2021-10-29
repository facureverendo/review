import os.path

import flask
from flask_cors import CORS

import app.domain.reviews.routes as review_routes
import app.domain.scores.routes as score_routes
import app.gateway.rabbit as rabbit_service
import app.utils.config as config


def _init_rabbit():
    rabbit_service.init()


def _generate_api_doc():
    os.system("apidoc -i app/ -o ./public")


class MainApp:
    def __init__(self):
        self.flask_app = flask.Flask(__name__, static_folder='../public')
        flask.current_app = self.flask_app
        CORS(self.flask_app, supports_credentials=True, automatic_options=True)

        _generate_api_doc()
        self._init_routes()
        _init_rabbit()
        self._init_reviews()
        self._init_scores()

    def _init_routes(self):
        @self.flask_app.route('/<path:path>')
        def api_index(path):
            return flask.send_from_directory('../public', path)

        @self.flask_app.route('/')
        def index():
            return flask.send_from_directory('../public', "index.html")

    def _init_reviews(self):
        review_routes.init(self.flask_app)

    def _init_scores(self):
        score_routes.init(self.flask_app)

    def get_flask_app(self):
        return self.flask_app

    def start(self):
        self.flask_app.run(port=config.get_server_port())
