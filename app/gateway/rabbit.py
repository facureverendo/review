import threading
import pika

import app.utils.config as config
import app.utils.json_serializer as json
import app.utils.schema_validator as validator
import app.utils.security as security

EVENT = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    }
}

MSG_NEW_SCORE = {
    "id_article": {
        "required": True,
        "type": str
    },
    "score": {
        "required": True,
        "type": float
    }
}


def init():
    auth_consumer = threading.Thread(target=listen_auth)
    auth_consumer.daemon = True
    auth_consumer.start()


def listen_auth():
    """
    Escucha eventos de logout provenientes de Auth para borrar tokens del cache.

    @api {fanout} auth/logout Logout

    @apiGroup RabbitMQ GET

    @apiDescription Escucha eventos de logout provenientes de Auth para borrar tokens del cache.

    @apiExample {json} Mensaje
      {
        "type": "article-exist",
        "message" : "tokenId"
      }
    """
    exchange = "auth"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type='fanout')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=exchange, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.body_to_dic(body.decode('utf-8'))
            if len(validator.validateSchema(EVENT, event)) > 0:
                return

            if event["type"] == "logout":
                security.invalidate_session(event["message"])

        print("RabbitMQ Auth conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception:
        print("RabbitMQ Auth desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, init).start()


def send_new_score(id_article, score):
    """
    Envía eventos cuando hay un nuevo score para un artículo

    @api {fanout} score/new_score Nuevo Score

    @apiGroup RabbitMQ POST

    @apiDescription Enviá mensajes de nuevo score

    @apiSuccessExample {json} Mensaje
      {
        "type": "new_score",
        "message" : {
            "id_article": "{id del articulo}",
            "score": {score promedio del articulo}
        }
      }
    """
    exchange = "score"
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get_rabbit_server_url()))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    message = {
        "type": "new_score",
        "message": {
            "id_article": id_article,
            "score": score,
        }
    }

    validator.validateSchema(MSG_NEW_SCORE, message)

    channel.basic_publish(exchange=exchange, routing_key='', body=json.dic_to_json(message))

    connection.close()

    print("RabbitMQ Cart POST new_score id_article:%r", id_article)
