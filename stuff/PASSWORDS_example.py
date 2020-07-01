DEBUG = True

settings = dict(
    telegram_bot_url1='xxx',  # Бот (БотШГ) 
    telegram_bot_url2='xxx',  # Бот (БотДШ) 
    telegram_chats_1=[xxx,   # 
                      xxx],  # 
    ymail_login='xxx',
    ymail_password='xxx',
    default_ymail_password='xxx',
    token_yandex='xxx',
    gtp_mail_robot_ID='xxx',
    gtp_mail_robot_password='xxx',
    gtp_mail_robot_callback='xxx',
    postgres_dbname='xxx',
    postgres_host='xxx',
    postgres_port='xxx',
    postgres_user='xxx',
    postgres_password='xxx',
    zoom03_api_key='xxx',
    zoom03_api_secret='xxx',
    zoom08_api_key='xxx',
    zoom08_api_secret='xxx',
    zoom09_api_key='xxx',
    zoom09_api_secret='xxx',
    zoom10_api_key='xxx',
    zoom10_api_secret='xxx',
    zoom11_api_key='xxx',
    zoom11_api_secret='xxx',
    zoom12_api_key='xxx',
    zoom12_api_secret='xxx',
    getcourse_login_page="xxx",
    getcourse_login="xxx",
    getcourse_password="xxx",
    bitrix_clientId="xxx",
    bitrix_clientCode="xxx",
    bitrix_clientSecret="xxx",
    bitrix_domainName="xxx",
    admin_emails=['xxx'],
    manager_emails=['xxx', 'xxx'],
    full_list_participants_to_emails=['xxx', 'xxx']
)

if DEBUG:
    settings_debug = dict(
        manager_emails=['xxx'],
        full_list_participants_to_emails=['xxx']
    )
    # print(settings)
    # merge dictionary Python 3.5 or greater (https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python)
    settings = {**settings, **settings_debug}


if __name__ == '__main__':
    print(settings)
