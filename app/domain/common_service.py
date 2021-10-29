import http.client
import socket
import app.utils.config as config
import app.utils.errors as errors
import app.utils.json_serializer as json


def get_article(id_article):
    conn = http.client.HTTPConnection(
        socket.gethostbyname(config.get_catalog_server_url()),
        config.get_catalog_server_port(),
    )

    try:
        conn.request("GET", "/v1/articles/{}".format(id_article), {})
        response = conn.getresponse()
        if response.status != 200 or (not json.body_to_dic(response.read().decode('utf-8'))['enabled']):
            raise errors.InvalidArgument('id_article', 'Invalido')
        return json.dic_to_json(response.read().decode('utf-8'))
    except Exception:
        raise Exception


def get_order(token, id_article):
    conn = http.client.HTTPConnection(socket.gethostbyname(config.get_order_server_url()),
                                      config.get_order_server_port())

    try:
        headers = {"Authorization".encode("utf-8"): token.encode("utf-8")}

        conn.request("GET", "/v1/orders", {}, headers)
        response = conn.getresponse()
    except Exception:
        raise Exception

    if response.status == 200:
        for obj in json.body_to_dic(response.read().decode('utf-8')):
            if obj['status'] == 'PLACED':
                order = get_specific_order(token, obj['id'], id_article)
                if order != "":
                    return order
        raise errors.InvalidRequest('No existen ordenes pagadas para este articulo')
    else:
        raise errors.InvalidRequest("Invalid Request")


def get_specific_order(token, id_order, id_article):
    headers = {"Authorization".encode("utf-8"): token.encode("utf-8")}
    conn = http.client.HTTPConnection(socket.gethostbyname(config.get_order_server_url()),
                                      config.get_order_server_port())

    try:
        conn.request("GET", "/v1/orders/{}".format(id_order), {}, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise errors.InvalidRequest('No existe una orden con ese id')
        else:
            order = json.body_to_dic(response.read().decode('utf-8'))
            for article in order['articles']:
                if article['id'] == id_article:
                    return order
            return ""
    except Exception:
        raise Exception
