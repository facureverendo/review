import flask

import app.domain.scores.score_service as service
import app.domain.scores.rest_validations as rest_validator
import app.domain.common_service as common_service
import app.utils.errors as errors
import app.utils.json_serializer as json
import app.utils.security as security


def init(app):

    @app.route('/v1/scores/<string:id_article>', methods=['POST'])
    def create_score(id_article):
        user = security.isValidToken(flask.request.headers.get("Authorization"))
        parameters = json.body_to_dic(flask.request.data)
        parameters.update({'id_article': id_article})
        parameters = rest_validator.validateAddorEditScore(parameters)
        common_service.get_article(id_article)
        common_service.get_order(flask.request.headers.get("Authorization"), id_article)
        result = service.add_score(parameters, user["id"])
        return json.dic_to_json(result)

    @app.route('/v1/scores/<string:id_article>', methods=['DELETE'])
    def delete_score(id_article):
        user = security.isValidToken(flask.request.headers.get("Authorization"))
        common_service.get_article(id_article)
        common_service.get_order(flask.request.headers.get("Authorization"), id_article)
        result = service.disable_score(id_article, user['id'])
        return json.dic_to_json(result)

    @app.route('/v1/scores/<string:id_article>', methods=['GET'])
    def get_score(id_article):
        security.isValidToken(flask.request.headers.get("Authorization"))
        common_service.get_article(id_article)
        result = service.get_score_article(id_article)
        return json.dic_to_json(result)

    @app.errorhandler(Exception)
    def handle_errors(err):
        return errors.handleError(err)