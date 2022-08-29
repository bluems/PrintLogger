from datetime import datetime
import sys
import subprocess
import pytz
import logging
import logging.handlers

from logging.handlers import TimedRotatingFileHandler

try:
    from rich.logging import RichHandler
except:
    subprocess.check_call([
        sys.executable,
        '-m', 'pip', 'install', '--upgrade', 'rich'
    ])
    from rich.logging import RichHandler


class PrintLogger:
    LOG_PATH = None
    RICH_FORMAT = "[%(filename)s:%(lineno)s] >> %(message)s"
    FILE_HANDLER_FORMAT = "[%(asctime)s]\t%(levelname)s\t[%(filename)s:%(funcName)s:%(lineno)s]\t>> %(message)s"

    _logger: logging.Logger = None

    class TimeFormatter(logging.Formatter):
        """Setting internal time zone in logging.Formatter"""
        timezone = 'Asia/Seoul'
        def converter(self, timestamp):
            dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
            return dt.astimezone(pytz.timezone(self.timezone))

        def formatTime(self, record, datefmt=None):
            dt = self.converter(record.created)
            if datefmt:
                s = dt.strftime(datefmt)
            else:
                try:
                    s = dt.isoformat(timespec='milliseconds')
                except TypeError:
                    s = dt.isoformat()
            return s


    @staticmethod
    def set_logger(logging_level, logging_path: str="./log.log", logging_type: str="time", tz = None, formatter_tz = None):
        if PrintLogger._logger is not None:
            pass
        else:
            if tz is not None:
                # Setting Global TimeZone
                """
                This parameter 'tz' does not directly modify the server's time zone.
                Changes the global time zone to be used by the current Python runtime.
                This is useful when the server's time zone affects other programs.
                """
                import os, time
                os.environ['TZ'] = tz
                time.tzset()
                PrintLogger.TimeFormatter.timezone = tz
            
            if formatter_tz is not None:
                PrintLogger.TimeFormatter.timezone = formatter_tz

            logging.basicConfig(
                level = logging_level,
                format = PrintLogger.RICH_FORMAT,
                handlers=[RichHandler(rich_tracebacks=True)]
            )

            logger = logging.getLogger ("rich")

            if logging_type == "time":
                PrintLogger.file_handler = PrintLogger._gen_time_handler(logging_path)
            else:
                PrintLogger.file_handler = PrintLogger._gen_file_handler(logging_path)

            PrintLogger.LOG_PATH = logging_path
            PrintLogger.file_handler.setFormatter(PrintLogger.TimeFormatter(PrintLogger.FILE_HANDLER_FORMAT))
            logger.addHandler(PrintLogger.file_handler)

            PrintLogger._logger = logger

    @staticmethod
    def _gen_file_handler(path: str) -> logging.FileHandler:
        return logging.FileHandler(
            path,
            mode = "a",
            encoding="utf-8"
        )

    @staticmethod
    def _gen_time_handler(path: str):
        handler = TimedRotatingFileHandler(
            path,
            when = "midnight",
            interval=1,
            encoding="utf-8"
        )
        handler.suffix = '-%Y%m%d'
        return handler

    @staticmethod
    def change_handler(path: str, logging_type: str="time"):
        PrintLogger._logger.disabled = True
        PrintLogger._logger.removeHandler(PrintLogger.file_handler)
        PrintLogger.file_handler.close()

        if logging_type == "time":
            PrintLogger.file_handler = PrintLogger._gen_time_handler(path)
        else:
            PrintLogger.file_handler = PrintLogger._gen_file_handler(path)

        PrintLogger.LOG_PATH = path
        PrintLogger.file_handler.setFormatter(PrintLogger.TimeFormatter(PrintLogger.FILE_HANDLER_FORMAT))
        PrintLogger._logger.addHandler(PrintLogger.file_handler)
        PrintLogger._logger.disabled = False
        
    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        PrintLogger._logger.error(
            "Unexpected exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    @staticmethod
    def debug(msg, *args, **kwargs):
        PrintLogger._logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        PrintLogger._logger.info(msg, *args, **kwargs)
    
    @staticmethod
    def warning(msg, *args, **kwargs):
        PrintLogger._logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        PrintLogger._logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        PrintLogger._logger.exception(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        PrintLogger._logger.critical(msg, *args, **kwargs)

    @staticmethod
    def log(level, msg, *args, **kwargs):
        PrintLogger._logger.log(level, msg, *args, **kwargs)
