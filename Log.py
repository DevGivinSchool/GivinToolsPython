import logging
import os


class Log:
    """Kласс для логирования"""
    LEVEL = logging.DEBUG

    @staticmethod
    def setup_logger(name, file_name, level=LEVEL):
        """Create custom loggers.
        :param str name: Name of logger.
        :param str file_name: File that logger writes to.
        :param level: Logging level.
        :return llogger: The custom logger.
        """
        log_dir = r"c:\!SAVE\log"
        log_file = os.path.join(log_dir, file_name)
        log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')
        handler = logging.FileHandler(log_file, mode='w')
        handler.setFormatter(log_formatter)
        llogger = logging.getLogger(name)
        llogger.setLevel(level)
        llogger.addHandler(handler)
        return llogger
