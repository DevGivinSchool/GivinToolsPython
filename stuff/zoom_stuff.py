import json
import zoom_us
import requests


def zoom_users_password(login, password):
    payload = {
        "password": password}
    payload = json.dumps(payload)
    # logger.debug(f"payload={payload}")
    headers = zoom_us.get_headers()
    # logger.debug(f"headers={headers}")
    url = zoom_us.zoom_api_endpoint_client_url + "/" + login + "/password"
    # print(f"url={url}")
    response = requests.request("PUT", url, data=payload, headers=headers)
    # if logger.level == 10:
    #     debug_text = "\n" + response.text + "\n" + \
    #                  f"response={response}\n" + \
    #                  f"response.headers={response.headers}\n" + \
    #                  f"response.request.headers={response.request.headers}\n" + \
    #                  f"response.request.path_url={response.request.path_url}\n" + \
    #                  f"response.text={response.text}\n" + \
    #                  f"response.url={response.url}\n" + \
    #                  f"response.status_code={response.status_code}\n" + \
    #                  f"response.ok={response.ok}"
    #     # print(debug_text)
    #     logger.debug(debug_text)
    # 200 и 204 = ОК если нет тогда из str:response.text можно вытащить дополнительный код и сообщение
    if response.ok:
        # logger.debug("Изменение статуса = ОК")
        return None
    else:
        # logger.error(f"ERROR:{response.text}")
        return response.text


def change_zoom_password(login, password):
    # print(login, password)
    if password.endswith('55'):
        # print(login, password)
        password = password[0:-2]
        r = zoom_users_password(login, password)
        if r is None:
            print(login, password)
        else:
            print(login, password, r)


if __name__ == '__main__':
    import csv

    file = r'd:\YandexDisk\TEMP\GS\change_password.csv'
    with open(file, newline='') as f:
        reader = csv.reader(f)
        # headers = next(reader, None)
        for row in reader:
            # print(row)
            change_zoom_password(row[0], row[1])
