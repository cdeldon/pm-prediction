import os
from datetime import datetime

from simple_logger import Logger


class __Settings:
    def __init__(self):
        self.__current_dir = os.path.dirname(os.path.realpath(__file__))

        self.__pm_root_dir = os.path.abspath(os.path.join(self.__current_dir, os.pardir))
        self.__project_root_dir = os.path.abspath(
            os.path.join(self.__pm_root_dir, os.pardir))

        self.__data_dir = os.path.join(self.__project_root_dir, "data")

        self.__logging_dir = os.path.join(self.__project_root_dir, "logs")

    @property
    def project_root_dir(self):
        return self.__project_root_dir

    @property
    def pm_root_dir(self):
        return self.__pm_root_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def log_dir(self):
        return self.__logging_dir


class LogLevel:
    """Log levels used for the :class:`simple_logger.Logger` object."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    WARN = WARNING
    ERROR = "ERROR"
    FATAL = "FATAL"


def setup_logger(console_log_level: LogLevel = LogLevel.INFO,
                 file_log_level: LogLevel = LogLevel.DEBUG,
                 log_file_name: str = None):
    """Sets up the simple logger.
    :param console_log_level: Log level associated to the streaming log.
    :param file_log_level: Log level associated to the file log.
    :param log_file_name: If set, then the file log is written to this file.
    Otherwise a new log file will be created in the log directory returned by
    :attr:`Settings.log_dir <pm.settings.__Settings.log_dir>`.
    """
    if log_file_name is None:
        log_directory = Settings.log_dir
        name = "pm_logging{}.log".format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        log_file_name = os.path.join(log_directory, name)

    Logger.set_file_logging_level(file_log_level)
    Logger.set_log_file(log_file_name)
    Logger.set_console_logging_level(console_log_level)
    Logger.init()

    Logger.info("Logging to {} file.".format(log_file_name))


Settings = __Settings()

__all__ = ["Settings", "LogLevel", "setup_logger"]
