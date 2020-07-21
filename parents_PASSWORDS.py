DEBUG = True

settings = dict(
    telegram_bot_parents_url='https://api.telegram.org/bot1327787515:AAFgOKpSy94tVXrmwpn6iPpTSh1TvVMsFCM',  # @WeAreParentsBot
    telegram_chats=[-350301781],  # Группа тестирования ботов
    parents_dbname='parents',
    parents_host='45.80.70.226',
    parents_port='5432',
    parents_user='parents',
    parents_password='gBQ$4q$MS3a$',
    admin_emails=['ministrbob777@gmail.com']
)

if DEBUG:
    settings_debug = dict(
        admin_emails=['ministrbob777@gmail.com']
    )
    # print(settings)
    # merge dictionary Python 3.5 or greater (https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python)
    settings = {**settings, **settings_debug}


if __name__ == '__main__':
    print(settings)
