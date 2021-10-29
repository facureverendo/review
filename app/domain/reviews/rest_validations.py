import app.utils.errors as error
import app.utils.schema_validator as schemaValidator


REVIEW_ADD_UPDATE_SCHEMA = {
    "title": {
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "description": {
        "type": str,
        "minLen": 1,
        "maxLen": 2048
        },
    "id_article": {
        "required": True,
        "type": str,
    }
}


def validateAddorEditReview(params):
    """
    Valida los parametros para crear un objeto.\n
    params: dict<propiedad, valor> Review
    """
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(REVIEW_ADD_UPDATE_SCHEMA, params)
