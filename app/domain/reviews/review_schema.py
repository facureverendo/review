import datetime
import numbers

import app.utils.errors as errors
import app.utils.schema_validator as validator


REVIEW_DB_SCHEMA = {
    "title": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "description": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 2048
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


def new_review():
    return {
        "title": "",
        "description": "",
        "id_user": "",
        "id_article": "",
        "created": datetime.datetime.utcnow(),
        "updated": datetime.datetime.utcnow(),
        "active": True
    }


def validate_schema(document):
    err = validator.validateSchema(REVIEW_DB_SCHEMA, document)

    if len(err) > 0:
        raise errors.MultipleArgumentException(err)