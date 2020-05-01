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
    Процедура изменения статуса пользователя activate/deactivate - разблокировка/блокировка
    https://marketplace.zoom.us/docs/api-reference/zoom-api/users/userstatus
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


def bulk_user_status_change(list_fio, status, logger=None):
    for login in list_fio.splitlines():
        print(f"Попытка блокировки участника |{login}|")
        logger.info(f"Попытка блокировки участника |{login}|")
        # Измение статуса в zoom (блокировка участника)
        zoom_result = zoom_users_userstatus(login, status, logger=logger)
        print(zoom_result)
        logger.debug(f"zoom_result={zoom_result}")
        if zoom_result is not None:
            logger.error("+" * 60)
            mail_text = f"\nПроцедура не смогла автоматически заблокировать участника. Ошибка:\n" \
                        f"{zoom_result}" \
                        f"\nLogin: {login}"
            # send_mail(PASSWORDS.logins['admin_emails'], "BLOCK PARTICIPANT ERROR", mail_text, logger)
            # print(mail_text)
            logger.error(mail_text)
            logger.error("+" * 60)
        else:
            print("Учётка Zoom успешно заблокирована")
            logger.info("Учётка Zoom успешно заблокирована")


def zoom_users_users(page_number, page_size, status, logger=None):
    """
    Получение списка участников
    :param page_number: Номер страницы
    :param page_size: Количество пользователей на странице
    :param status: Статус участника active/inactive
    :param logger: Логгер
    :return:
    """
    # def zoom_users_users(page_count, page_number, page_size, status, logger=None):
    # querystring = {"page_count": page_count, "page_number": page_number, "page_size": page_size, "status": status}
    querystring = {"page_number": page_number, "page_size": page_size, "status": status}
    # querystring = {"page_size": page_size, "status": status}
    # querystring = {"page_size": page_size}
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


def list_meetings(gwt, userid, page_number, page_size, mtype, logger=None):
    """
    Получение списка встреч
    :param userid:
    :param page_number: Номер страницы
    :param page_size: Количество пользователей на странице
    :param logger: Логгер
    :return:
    """
    """
    Возможны такие типы встреч. Я пока использую scheduled
    The meeting types: 
    scheduled - This includes all valid past meetings (unexpired), live meetings and upcoming scheduled meetings. It is equivalent to the combined list of “Previous Meetings” and “Upcoming Meetings” displayed in the user’s Meetings page on the Zoom Web Portal. 
    scheduled = live + upcoming [Те которые есть + которые уже прошли]
    live - All the ongoing meetings. [Текущие встречи] 
    upcoming - All upcoming meetings including live meetings. [Предстоящие встречи (те которые как раз и есть)]
    """
    # def zoom_users_users(page_count, page_number, page_size, status, logger=None):
    # querystring = {"page_count": page_count, "page_number": page_number, "page_size": page_size, "status": status}
    querystring = {"userid": userid, "page_number": page_number, "page_size": page_size, "type": mtype}
    # querystring = {"page_size": page_size, "status": status}
    # querystring = {"page_size": page_size}
    # При этом возвращается
    # "page_count": 12, "page_number": 1, "page_size": 30, "total_records": 331
    logger.debug(f"querystring={querystring}")
    headers = get_headers(gwt)
    logger.debug(f"headers={headers}")
    url = zoom_api_endpoint_client_url + "/" + userid + "/meetings"
    # print(url)
    response = requests.request("GET", url, headers=headers, params=querystring)
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


def list_meetings_for_user(gwt, userid, meeting_type, logger=None):
    """
    Получение списка встреч для конкретного пользователя
    :param userid:
    :param meeting_type:
    :param logger:
    :return:
    """
    lm = []
    # userid = 'zoom06@givinschool.org'
    # meeting_type = "scheduled"  # =6
    # meeting_type = "live"  # =0
    # meeting_type = "upcoming"  # =3
    # Полный вызов
    # response = eval(zoom_users_users(page_count=3, page_number=1, page_size=1, status='active', logger=logger))
    # Выборка одной строки, только для того, чтобы получить общее количество записей.
    response = eval(list_meetings(gwt, userid, page_number=1, page_size=1, mtype=meeting_type, logger=logger))
    # Вот такой ответ получается, response={'page_count': 24, 'page_number': 1, 'page_size': 1, 'total_records': 24,
    # 'meetings': [{'uuid': 'VMLPL4s2S5Se1e+rLwrd7w==', 'id': 618717733, 'host_id': 'IS5Fgs4XTEa-dknKFzNQWw',
    # 'topic': 'ПТО  24.09-.05.10.2019', 'type': 8, 'start_time': '2019-09-28T05:00:00Z', 'duration': 240,
    # 'timezone': 'Europe/Moscow', 'created_at': '2019-09-28T04:51:36Z', 'join_url':
    # 'https://givinschool.zoom.us/j/618717733'}]}
    # print(f"response={response}")
    # print(f'total_records={response["total_records"]}')
    page_count = math.ceil(response["total_records"] / 300)
    # print(f"page_count={page_count}")
    for page in range(1, page_count + 1):
        # print(f"page={page}")
        response = eval(list_meetings(gwt, userid, page_number=page, page_size=300, mtype=meeting_type, logger=logger))
        for meet in response["meetings"]:
            # print(meet)
            # {'uuid': 'VMLPL4s2S5Se1e+rLwrd7w==', 'id': 618717733, 'host_id': 'IS5Fgs4XTEa-dknKFzNQWw',
            # 'topic': 'ПТО  24.09-.05.10.2019', 'type': 8, 'start_time': '2019-09-28T05:00:00Z', 'duration': 240,
            # 'timezone': 'Europe/Moscow', 'created_at': '2019-09-28T04:51:36Z', 'join_url':
            # 'https://givinschool.zoom.us/j/618717733'}
            id_ = str(meet["id"])
            id_ = id_[0:3] + "-" + id_[3:6] + "-" + id_[6:]
            curr = ""
            try:
                if meet["type"] != 3:
                    curr = f'{(meet["topic"]).ljust(30, " ")} - {id_.ljust(15, " ")} - {meet["join_url"].ljust(45, " ")} - {meet["start_time"]}'
                    # print(f'type={meet["type"]}|{meet["topic"]} - {id_} - {meet["join_url"]} - {meet["start_time"]}')
                    # print(curr)
                else:
                    curr = f'{meet["topic"].ljust(30, " ")} - {id_.ljust(15, " ")} - {meet["join_url"].ljust(45, " ")}'
                    # print(f'type={meet["type"]}|{meet["topic"]} - {id_} - {meet["join_url"]}')
                    # print(curr)
                lm.append(curr)
            except:
                print("ERROR")
                print(f"meet={meet}")
                print(traceback.format_exc())
            finally:
                # print("=" * 120)
                pass
    return lm


def print_list_meetings_for_user(gwt, userid, meeting_type, logger):
    print(userid)
    lm = list_meetings_for_user(gwt=gwt, userid=userid, meeting_type=meeting_type, logger=logger)
    for m in lm:
        print(f"    {m}")


def get_headers(gwt):
    bearer = "Bearer " + gwt
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


# ==========================================================================================
"""
if __name__ == '__main__':
    # Создание Bearer
    print(generate_jwt(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret']))
"""
# ==========================================================================================
"""
    # Создание пользователя Zoom
    import logging
    from Log import Log
    from log_config import log_dir, log_level
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us.log', logging.DEBUG)
    response = zoom_users_create("test777_test777@givinschool.org",
                                 "Дмитрий",
                                 "Салтыков Щедрин",
                                 "ANps11CDkz",
                                 logger=logger)
    print(response)
"""
# ==========================================================================================
"""
if __name__ == '__main__':
    # Список участников (можно получить только простых участников
    # https://marketplace.zoom.us/docs/api-reference/zoom-api/users/users
    import logging
    from datetime import datetime
    from Log import Log
    from log_config import log_dir, log_level

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us_{now}.log', logging.DEBUG)
    # Полный вызов
    # response = eval(zoom_users_users(page_count=3, page_number=1, page_size=1, status='active', logger=logger))
    # Выборка одной строки, только для того, чтобы получить общее количество записей.
    response = eval(zoom_users_users(page_number=1, page_size=1, status='active', logger=logger))
    # Вот такой ответ получается,
    # response={'page_count': 334, 'page_number': 1, 'page_size': 1, 'total_records': 334, 'users': [...
    print(f"response={response}")
    import math

    print(f'total_records={response["total_records"]}')
    page_count = math.ceil(response["total_records"] / 300)
    print(f"page_count={page_count}")
    user_list = []
    i = 1
    for page in range(1, page_count + 1):
        # print(f"page={page}")
        response = eval(zoom_users_users(page_number=page, page_size=300, status='active', logger=logger))
        for user in response["users"]:
            # print(user)
            # {'id': 'IS5Fgs4XTEa-dknKFzNQWw', 'first_name': 'Школа Гивина 03', 'last_name': 'ПТО созвоны 300',
            #  'email': 'zoom03@givinschool.org', 'type': 2, 'pmi': 5747735781, 'timezone': 'Europe/Moscow',
            #  'verified': 1, 'dept': '', 'created_at': '2019-07-20T12:07:24Z', 'last_login_time': '2020-04-29T12:42:20Z',
            #  'last_client_version': '4.6.20553.0413(android)',
            #  'pic_url': 'https://givinschool.zoom.us/p/IS5Fgs4XTEa-dknKFzNQWw/f0f0bb1b-b018-4329-9ad8-f6d75ac485f7-6215',
            #  'language': 'ru-RU', 'phone_number': '+7 ', 'status': 'active'}
            # type {1:Basic, 2:Licensed, 3:On-prem}
            if user["type"] == 1:  # Print only Basic users
                print(f'{i}|{user["email"]}|{user["status"]}|{user["type"]}')
                i += 1
            else:  # List type = 2:Licensed, 3:On-prem - zoom03
                user_list.append(user)
    # PRINT # List type = 2:Licensed, 3:On-prem - zoom03
    # print(user_list)
    print("=" * 120)
    for user in user_list:
        print(f'{i}|{user["email"]}|{user["status"]}|{user["type"]}|{user["id"]}')
        i += 1
"""
# ==========================================================================================
"""
    # Блокировка пользователей zoom по списку логинов
    import logging
    from datetime import datetime
    from Log import Log
    from log_config import log_dir, log_level
    from list_ import list_fio

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us_{now}.log', logging.DEBUG)
    action = 'deactivate'
    bulk_user_status_change(list_fio, action, logger)
"""
# ==========================================================================================

if __name__ == '__main__':
    # Список встреч
    # https://marketplace.zoom.us/docs/api-reference/zoom-api/users/users
    import logging
    import traceback
    import math
    import datetime
    from Log import Log
    from log_config import log_dir, log_level

    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'zoom_us_{now}.log', logging.DEBUG)
    print(f"Текущие встречи на {datetime.date.today()}:\n")
    list_users = ['zoom01@givinschool.org', 'zoom02@givinschool.org', 'zoom03@givinschool.org',
                  'zoom04@givinschool.org', 'zoom05@givinschool.org', 'zoom06@givinschool.org',
                  'zoom07@givinschool.org']
    gwt = generate_jwt(PASSWORDS.logins['zoom03_api_key'], PASSWORDS.logins['zoom03_api_secret'])
    for lu in list_users:
        print_list_meetings_for_user(gwt=gwt, userid=lu, meeting_type="upcoming", logger=logger)
    zoom_user08 = 'zoom08@givinschool.org'
    gwt = generate_jwt(PASSWORDS.logins['zoom08_api_key'], PASSWORDS.logins['zoom08_api_secret'])
    print_list_meetings_for_user(gwt=gwt, userid=zoom_user08, meeting_type="upcoming", logger=logger)
    zoom_user09 = 'zoom09gs@gmail.com'
    gwt = generate_jwt(PASSWORDS.logins['zoom09_api_key'], PASSWORDS.logins['zoom09_api_secret'])
    print_list_meetings_for_user(gwt=gwt, userid=zoom_user09, meeting_type="upcoming", logger=logger)
