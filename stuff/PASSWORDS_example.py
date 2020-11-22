import pprint
# PASSWORDS.settings['postgres_dbname']
DEBUG = True
# PROFILE = DEV, PROD
PROFILE = 'PROD'

settings = dict(
    list_path=r'c:\MyGit\GivinToolsPython\list.txt',
    django_secret_key=r'xxx',
    # chromedriver_path=r"c:\Users\MinistrBob\.wdm\drivers\chromedriver\85.0.4183.87\win32\chromedriver.exe",
    # chromedriver path
    # headless=False,  # chromedriver headless
    # telegram_id=1777776,
    # telegram_hash="79b3ab66b6e8f7777b5fb849ee342a66",
    # Бот (БотШГ) @GivinSchoolBot
    telegram_bot_url1='https://api.telegram.org/bot510777777:AAGSy__40rfJieD2QSxTcXm-pk4h45XXAH8',
    # Бот (БотДШ) @GivinSchoolSFBot
    telegram_bot_url2='https://api.telegram.org/bot100777777:AAHRLBbspE4GillGlyQZQtehPn5gk3xTZXA',
    telegram_chats_1=[{'chat_id': -1001277777777, 'chat_name': 'Название чата 1'},
                      {'chat_id': -1001177777777, 'chat_name': 'Название чата 2'}],
    ymail_login='ymail_login@givinschool.org',
    ymail_password='xxx',
    default_ymail_password='xxx',
    token_yandex='AgAEA9qi7nH4XWZrt5e0UXPzjkMerda2EkZeC4k',
    gtp_mail_robot_ID='466d54d024f54346915657655a4e9c33',
    gtp_mail_robot_password='ec7846c22a6343619873ef7a04ee2457',
    gtp_mail_robot_callback='https://oauth.yandex.ru/verification_code',
    zoom03_api_key='VJwEVENaTdttTMKXSuYNaA',
    zoom03_api_secret='h6Wg6areKuGJFRYBHTDmjtfozmbN9cmDnonf',
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
    getcourse_login_page="https://givinschoolru.getcourse.ru/cms/system/login",
    getcourse_login="getcourse_login@givinschool.org",
    getcourse_password="xxx",
    getcourse_key="eWEuXoPxih6KU28tm45jndfnb875nvTFbutk8grXUhbH4X5bBUpx6cTjzv5v3ySXedflkrutnHFRndT4668rAOAcsJjt6GrB9cSzflAjDUBnQSvAqzpKCt1FU60F2",
    bitrix_clientId="777",
    bitrix_clientCode="local.5d2a5834b949b0.48729573",
    bitrix_clientSecret="nJPDHkLog6QCJTptynds7eGTbd34GbHckj955t0dFLN1S",
    bitrix_domainName="newhuman.bitrix24.ru",
    admin_emails=['xxx@gmail.com'],
    #
    postgres_dbname_src='gs_dev',
    postgres_dbname_dst='gs_dev',
    table_name_src="team_members",
    table_name_dst="gtp_teammember",
)

if PROFILE == 'PROD':
    settings_debug = dict(
        chromedriver_path=r"/usr/local/bin/chromedriver",  # chromedriver path
        headless=True,  # chromedriver headless
        postgres_dbname='gs',
        postgres_host='127.0.0.1',
        postgres_port='5432',
        postgres_user='postgres_user',
        postgres_password='xxx',
        django_secret_key=r'xxx',
        admin_emails=['xxx@gmail.com'],
        manager_emails=['xxx@gmail.com', 'xxx@hotmail.com'],
        full_list_participants_to_emails=['xxx@givinschool.org', 'xxx@mail.ru', 'xxx@hotmail.com']
    )

if PROFILE == 'DEV':
    settings_debug = dict(
        list_path=r'c:\MyGit\GivinToolsPython\list.txt',
        postgres_dbname='gs_dev',
        postgres_host='127.0.0.1',
        postgres_port='5432',
        postgres_user='postgres_user',
        postgres_password='xxx',
        manager_emails=['xxx@gmail.com'],
        full_list_participants_to_emails=['xxx@gmail.com']
    )
    # print(settings)
    # merge dictionary Python 3.5 or greater (https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python)

settings = {**settings, **settings_debug}

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(settings_debug)
    pp.pprint(settings)
