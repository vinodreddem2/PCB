import os
import logging
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler
import time
import smtplib
import warnings
warnings.simplefilter('always', DeprecationWarning)


class SizedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """

        # Size based rotation condition
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1

        # Time based rotation condition
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level


class ExperimentalFeatureWarning(Warning):
    pass


class ArgumentError(Exception):

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


def prepare_log_directory(log_name, log_directory):
    """

    Function to prepare directory structure

    :return: Path of log directory
    :rtype: str

    """
    try:
        base_logs_path = log_directory
        if not os.path.exists(base_logs_path):
            os.mkdir(base_logs_path)

        logs_file_path = os.path.join(base_logs_path, log_name)

        if not os.path.exists(logs_file_path):            
            os.mkdir(logs_file_path)

        if not os.path.exists(os.path.join(logs_file_path, 'Error')):
            os.mkdir(os.path.join(logs_file_path, 'Error'))

        if not os.path.exists(os.path.join(logs_file_path, 'Debug')):
            os.mkdir(os.path.join(logs_file_path, 'Debug'))

        if not os.path.exists(os.path.join(logs_file_path, 'Info')):
            os.mkdir(os.path.join(logs_file_path, 'Info'))

        if not os.path.exists(os.path.join(logs_file_path, 'Warning')):
            os.mkdir(os.path.join(logs_file_path, 'Warning'))

        return logs_file_path

    except Exception:
        exception_message = traceback.format_exc()
        raise NotADirectoryError('Unable to make logging directory structure. Details: %s' % str(exception_message))


def init_logging(log_name='logger', log_directory='logs', log_mode='a', max_bytes=100 * 1024 * 1024,
                 rotate_when='d', rotate_interval=1, backup_count=20, encoding=None, delay=0,
                 log_level='INFO', console_log=True, rotation_criteria='size',
                 log_format='[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - Line no - %(lineno)d '
                            '-- %(message)s\n'):
    """

    Function to initialize logging library with log rotation feature enabled.

    Please note, arguments related to log rotation depends on the chosen rotation criteria.

    For rotation criteria == 'size', 'log_mode' & 'max_bytes' are required.
    For rotation criteria == 'time', 'rotate_when' & 'rotate_interval' are required

    :param log_name: Name of log
    :type log_name: str
    :param log_directory: Directory for saving log files
    :type log_directory: str
    :param log_mode: Mode of logging. Options: Append('a') | Write ('w')
    :type log_mode: str
    :param max_bytes: Max file size
    :type max_bytes: int
    :param rotate_when: When to rotate. Options: day('d') | hour('h') | minute('m') | seconds('s')
    :type rotate_when: str
    :param rotate_interval: Interval for rotation
    :type rotate_interval: int
    :param backup_count: Number of backup files to keep on rotation
    :type backup_count: int
    :param encoding: Encoding scheme for logging
    :type encoding: str
    :param delay: Delay flag for logging.
    :type delay: int
    :param log_level: Log level. (DEBUG|INFO|WARNING|ERROR|CRITICAL)
    :type log_level: str
    :param console_log: Flag for turning console logging on or off.
    :type console_log: Boolean
    :param rotation_criteria: Type of rotation. Options: 'size' | 'time'
    :type rotation_criteria: str
    :param log_format: Log formatter for setting log pattern
    :type log_format: str
    :return: Logger object
    :rtype: Logger

    """

    try:
        logs_path = prepare_log_directory(log_name=log_name, log_directory=log_directory)

        log = logging.getLogger(log_name)
        log_formatter = logging.Formatter(log_format)

        # Adding log handler for logging on console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)

        # Variables for log paths for DEBUG, INFO, WARN, ERROR
        debug_log_file_name = os.path.join(os.path.join(logs_path, 'Debug'), (log_name + '.debug'))
        info_log_file_name = os.path.join(os.path.join(logs_path, 'Info'), (log_name + '.info'))
        warning_log_file_name = os.path.join(os.path.join(logs_path, 'Warning'), (log_name + '.warn'))
        error_log_file_name = os.path.join(os.path.join(logs_path, 'Error'), (log_name + '.error'))

        if rotation_criteria.lower() in ('timeandsize', 'sizeandtime'):
            warnings.warn('Using both time and size based rotation is in '
                          'experimental mode. \nPlease do not use in PROD environment',
                          category=ExperimentalFeatureWarning)
            debug_file_handler = SizedTimedRotatingFileHandler(debug_log_file_name, when=rotate_when,
                                                               interval=rotate_interval, backupCount=backup_count,
                                                               encoding=encoding, delay=delay, maxBytes=max_bytes)
            info_file_handler = SizedTimedRotatingFileHandler(info_log_file_name, when=rotate_when,
                                                              interval=rotate_interval, backupCount=backup_count,
                                                              encoding=encoding, delay=delay, maxBytes=max_bytes)
            warning_file_handler = SizedTimedRotatingFileHandler(warning_log_file_name, when=rotate_when,
                                                                 interval=rotate_interval, backupCount=backup_count,
                                                                 encoding=encoding, delay=delay, maxBytes=max_bytes)
            error_file_handler = SizedTimedRotatingFileHandler(error_log_file_name, when=rotate_when,
                                                               interval=rotate_interval, backupCount=backup_count,
                                                               encoding=encoding, delay=delay, maxBytes=max_bytes)
        elif rotation_criteria.lower() == 'time':
            # Log handlers for time based file rotation
            debug_file_handler = TimedRotatingFileHandler(debug_log_file_name, when=rotate_when,
                                                          interval=rotate_interval, backupCount=backup_count,
                                                          encoding=encoding, delay=delay)
            info_file_handler = TimedRotatingFileHandler(info_log_file_name, when=rotate_when,
                                                         interval=rotate_interval, backupCount=backup_count,
                                                         encoding=encoding, delay=delay)
            warning_file_handler = TimedRotatingFileHandler(warning_log_file_name, when=rotate_when,
                                                            interval=rotate_interval, backupCount=backup_count,
                                                            encoding=encoding, delay=delay)
            error_file_handler = TimedRotatingFileHandler(error_log_file_name, when=rotate_when,
                                                          interval=rotate_interval, backupCount=backup_count,
                                                          encoding=encoding, delay=delay)
        else:
            # Log handlers for size based file rotation
            debug_file_handler = RotatingFileHandler(debug_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)
            info_file_handler = RotatingFileHandler(info_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                    backupCount=backup_count, encoding=encoding, delay=delay)
            warning_file_handler = RotatingFileHandler(warning_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                       backupCount=backup_count, encoding=encoding, delay=delay)
            error_file_handler = RotatingFileHandler(error_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)

        # Setting log handler properties
        debug_file_handler.setFormatter(log_formatter)
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.addFilter(MyFilter(logging.DEBUG))

        info_file_handler.setFormatter(log_formatter)
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(MyFilter(logging.INFO))

        warning_file_handler.setFormatter(log_formatter)
        warning_file_handler.setLevel(logging.WARNING)
        warning_file_handler.addFilter(MyFilter(logging.WARNING))

        error_file_handler.setFormatter(log_formatter)
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.addFilter(MyFilter(logging.ERROR))

        # Adding log handlers to the log object if not already added
        # Checking is performed to prevent any duplicate addition of handlers
        if not len(log.handlers):

            if console_log:
                log.addHandler(stream_handler)

            log.addHandler(debug_file_handler)
            log.addHandler(info_file_handler)
            log.addHandler(warning_file_handler)
            log.addHandler(error_file_handler)

        # Checking if log level in 'str' format or 'int' format
        if isinstance(log_level, int):
            log.setLevel(log_level)
        else:
            log.setLevel(getattr(logging, log_level.upper()))

        return log

    except Exception:
        exception_message = traceback.format_exc()
        raise Exception('Error occurred in setting up logging. Details: %s' % str(exception_message))
