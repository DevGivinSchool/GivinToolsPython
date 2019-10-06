import logging
import os


class Log:
    """Kласс для логирования. log_level передаётся конструктор, по умолчанию logging.INFO"""

    @staticmethod
    def setup_logger(name, log_path=os.path.dirname(os.path.realpath(__file__)), log_name='log.log',
                     level=logging.INFO):
        """Create custom loggers.
        :param str name: Logger name.
        :param log_path: Directory that create log file.
        Логирование по умолчанию производится в папку где лежит скрипт/log
        :param str log_name: File that logger writes to.
        :param level: Logging level.
        :return custom_logger: The custom logger.
        """
        # Если директории для логирования не существует создаём её
        if not os.path.exists(log_path):
            try:
                os.mkdir(log_path)
            except OSError:
                print("Creation of the directory %s failed" % log_path)
                exit(1)
        log_file = ""
        try:
            log_file = os.path.join(log_path, log_name)
        except OSError:
            print(f"Creation of the log_file from log_path:'{log_path}' and log_name:'{log_name}' failed")
            exit(1)

        log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')
        handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        handler.setFormatter(log_formatter)
        custom_logger = logging.getLogger(name)
        custom_logger.setLevel(level)
        custom_logger.addHandler(handler)
        # print(custom_logger.handlers[0].baseFilename)
        return custom_logger
