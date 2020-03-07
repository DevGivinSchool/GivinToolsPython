import json
import PASSWORDS
import requests
import time
import jwt

zoom_api_base_url = "https://api.zoom.us/v2"
zoom_api_endpoint_client_url = zoom_api_base_url + "/users"


def zoom_users_usercreate(email, first_name, last_name, password, logger=None):
    """
    Процедура создания пользователя zoom
    :param email:
    :param first_name:
    :param last_name:
    :param password:
    :param logger:
    :return: При удачном создании пользователя
    {"id":"C1v4imjgTF6Ce0GQ89AaUw","first_name":"Дмитрий","last_name":"Салтыков Щедрин","email":"test777_test777@givinschool.org","type":1}
    response=<Response [201]>
    response.headers={'Date': 'Mon, 24 Feb 2020 16:25:05 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Content-Length': '156', 'Connection': 'keep-alive', 'Server': 'ZOOM', 'x-zm-trackingid': 'WEB_e681aa4e4c55a1acbc9fbd46f94f580a', 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-cache, no-store, must-revalidate, no-transform', 'Pragma': 'no-cache', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT', 'Set-Cookie': 'cred=2D7435E5E38A01DF79F90A1327FD9464; Path=/; Secure; HttpOnly', 'Strict-Transport-Security': 'max-age=31536000', 'X-XSS-Protection': '1; mode=block', 'Referrer-Policy': 'strict-origin-when-cross-origin'}
    response.request.headers={'User-Agent': 'python-requests/2.22.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'authorization': 'Bearer XXX', 'content-type': 'application/json', 'Content-Length': '282'}
    response.request.path_url=/v2/users
    response.text={"id":"C1v4imjgTF6Ce0GQ89AaUw","first_name":"Дмитрий","last_name":"Салтыков Щедрин","email":"test777_test777@givinschool.org","type":1}
    response.url=https://api.zoom.us/v2/users
    response.status_code=201

    """
    user = {
        "action": "autoCreate",
        "user_info": {
            "email": email,
            "type": 1,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        }
    }
    # print(f"user={user}")
    logger.debug(f"user={user}")
    user = json.dumps(user)
    # print(f"user josn={user}")
    logger.debug(f"user josn={user}")

    headers = get_headers()
    response = requests.request("POST", zoom_api_endpoint_client_url, data=user, headers=headers)

    if logger.level == 10:
        debug_text = "\n" + response.text + "\n" + \
                     f"response={response}\n" + \
                     f"response.headers={response.headers}\n" + \
                     f"response.request.headers={response.request.headers}\n" + \
                     f"response.request.path_url={response.request.path_url}\n" + \
                     f"response.text={response.text}\n" + \
                     f"response.url={response.url}\n" + \
                     f"response.status_code={response.status_code}\n" + \
                     f"response.ok={response.ok}"
        # print(debug_text)
        logger.debug(debug_text)
    # 201 = ОК если нет тогда из str:response.text можно вытащить дополнительный код и сообщение

    if response.ok:
        logger.debug("Пользователь создан = ОК")
        return None
    else:
        logger.error(f"ERROR:{response.text}")
        return response.text


def zoom_users_userstatus(login, action, logger=None):
    """
    Процедура изменения статуса пользователя activate/deactivate
    :param login: Login zoom
    :param action: activate/deactivate
    :param logger: logger
    :return:
    """
    payload = {
        "action": action}
    payload = json.dumps(payload)
    logger.debug(f"payload={payload}")
    headers = get_headers()
    logger.debug(f"headers={headers}")
    url = zoom_api_endpoint_client_url + "/" + login + "/status"
    logger.debug(f"url={url}")
    response = requests.request("PUT", url, data=payload, headers=headers)
    if logger.level == 10:
        debug_text = "\n" + response.text + "\n" + \
                     f"response={response}\n" + \
                     f"response.headers={response.headers}\n" + \
                     f"response.request.headers={response.request.headers}\n" + \
                     f"response.request.path_url={response.request.path_url}\n" + \
                     f"response.text={response.text}\n" + \
                     f"response.url={response.url}\n" + \
                     f"response.status_code={response.status_code}\n" + \
                     f"response.ok={response.ok}"
        # print(debug_text)
        logger.debug(debug_text)
    # 200 и 204 = ОК если нет тогда из str:response.text можно вытащить дополнительный код и сообщение
    if response.ok:
        logger.debug("Изменение статуса = ОК")
        return None
    else:
        logger.error(f"ERROR:{response.text}")
        return response.text


def zoom_users_users(page_count, page_number, page_size, status, logger=None):
    # querystring = {"page_count": page_count, "page_number": page_number, "page_size": page_size, "status": status}
    querystring = {"page_number": page_number, "page_size": page_size, "status": status}
    # querystring = {"page_size": page_size, "status": status}
    # При этом возвращается
    # "page_count": 12, "page_number": 1, "page_size": 30, "total_records": 331
    logger.debug(f"querystring={querystring}")
    headers = get_headers()
    logger.debug(f"headers={headers}")

    response = requests.request("GET", zoom_api_endpoint_client_url, headers=headers, params=querystring)
    if logger.level == 10:
        debug_text = "\n" + response.text + "\n" + \
                     f"response={response}\n" + \
                     f"response.headers={response.headers}\n" + \
                     f"response.request.headers={response.request.headers}\n" + \
                     f"response.request.path_url={response.request.path_url}\n" + \
                     f"response.text={response.text}\n" + \
                     f"response.url={response.url}\n" + \
                     f"response.status_code={response.status_code}\n" + \
                     f"response.ok={response.ok}"
        # print(debug_text)
        logger.debug(debug_text)
    if response.ok:
        logger.debug("ОК")
        return response.text
    else:
        logger.error(f"ERROR:{response.text}")
        return response.text


def get_headers():
    bearer = "Bearer " + generate_jwt(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])
    headers = {
        'authorization': bearer,
        'content-type': "application/json"
    }
    return headers


def generate_jwt(key, secret):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"iss": key, "exp": int(time.time() + 3600)}
    token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
    return token.decode("utf-8")


if __name__ == '__main__':
    """import logging
    from Log import Log
    from log_config import log_dir, log_level
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us.log', logging.DEBUG)
    response = zoom_users_create("test777_test777@givinschool.org",
                                 "Дмитрий",
                                 "Салтыков Щедрин",
                                 "ANps11CDkz",
                                 logger=logger)
    print(response)"""

    # print(generate_jwt(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret']))

    import logging
    from datetime import datetime
    from Log import Log
    from log_config import log_dir, log_level

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us_{now}.log', logging.DEBUG)
    response = eval(zoom_users_users(3, 1, 1, 'active', logger=logger))
    print(f"response={response}")
    import math

    print(response["total_records"])
    print(type(response["total_records"]))
    page_count = math.ceil(response["total_records"] / 300)
    user_list = []
    for page in range(1, page_count):
        response = eval(zoom_users_users(3, page, 300, 'pending', logger=logger))
        for user in response["users"]:
            print(f'{user["email"]}|{user["type"]}')
            if user["type"] == 2:
                 user_list.append(user["email"])
    print(user_list)
