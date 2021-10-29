import datetime

import app.utils.errors as errors
import app.utils.schema_validator as validator


SCORE_DB_SCHEMA = {
    "value": {
        "required": True,
        "type": int,
        "min": 0,
        "max": 10
        },
    "id_article": {
        "required": True,
        "type": str,
    },
    "id_user": {
        "requires": True,
        "type": str,
    }
}


def new_score():
    return {
        "value": 0,
        "id_user": "",
        "id_article": "",
        "created": datetime.datetime.utcnow(),
        "updated": datetime.datetime.utcnow(),
        "active": True
    }


def validate_schema(document):
    err = validator.validateSchema(SCORE_DB_SCHEMA, document)

    if len(err) > 0:
        raise errors.MultipleArgumentException(err)