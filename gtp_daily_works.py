import gtp_config
import PASSWORDS
import traceback
import sys
from Log import Log
from datetime import datetime
from alert_to_mail import send_mail


# Текущая дата для имени лог файла (без %S)
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', gtp_config.config['log_dir'], f'gtp_daily_works_{now}.log',
                          gtp_config.config['log_level'])
logger.info('START gtp_daily_works')


def main():
    try:
        pass
# TODO Два Уведомления всем о приближении срока платежа за 7 и за 3 дня. У вас оканчивает оплаченый период ДШ.
#  Вы можете оплатить прямо сейчас следующий период, он автоматически продлиться с конча текущего.
#  Если оплаивиать за 3 или 6 месяцев действют скидки 7??? и 8??? % соответсвенно.

# TODO Получение списка должников и его отправка менедджерам по почте
#  (пока вручную запросом и потом через выгрузку в TXT и в Excel)
#     в этот список включать пользователей без почты и телеграм

# TODO Процедура удаления пользователей у которых последний платёж год назад вместе со всеми их платёжками и письмами

# TODO Процедура удаления писем из почты старше 1 года
    except Exception:
        error_text = "MAIN ERROR:\n" + traceback.format_exc()
        print(error_text)
        logger.error(error_text)
        logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
        send_mail(PASSWORDS.logins['admin_emails'], "DAILY WORKS ERROR", error_text, logger)
        logger.error("Exit with error")
        sys.exit(1)
    logger.info('END gtp_daily_works')


if __name__ == "__main__":
    main()
