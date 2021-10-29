import app.utils.errors as error
import app.utils.schema_validator as schemaValidator


SCORE_ADD_UPDATE_SCHEMA = {
    "value": {
        "type": int,
        "min": 1,
        "max": 10
        },
    "id_article": {
        "required": True,
        "type": str,
    }
}


def validateAddorEditScore(params):
    """
    Valida los parametros para crear un objeto.\n
    params: dict<propiedad, valor> Review
    """
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(SCORE_ADD_UPDATE_SCHEMA, params)