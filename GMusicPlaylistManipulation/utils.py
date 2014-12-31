import os
import appdirs
import errno
import logging
import time

def logger(name, console_loglevel = 'INFO', file_loglevel = 'INFO'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # create null handler if running silent
    if console_loglevel == 'NONE' and file_loglevel == 'NONE':
        nh = logging.NullHandler()
        log.addHandler(nh)

    # set up console logging
    if console_loglevel != 'NONE':
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

        if console_loglevel == 'CRITICAL':
            ch.setLevel(logging.CRITICAL)
        elif console_loglevel == 'ERROR':
            ch.setLevel(logging.ERROR)
        elif console_loglevel == 'WARNING':
            ch.setLevel(logging.WARNING)
        elif console_loglevel == 'DEBUG':
            ch.setLevel(logging.DEBUG)
        else: ch.setLevel(logging.INFO)

        log.addHandler(ch)

    # set up file logging
    if file_loglevel != 'NONE':
        log_path = os.path.join(appdirs.user_log_dir(name), name + '.log')
        try:
            os.makedirs(os.path.dirname(log_path), 0o700)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        fh = logging.FileHandler(log_path)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s [%(levelname)s]: %(message)s'))

        if file_loglevel == 'CRITICAL':
            fh.setLevel(logging.CRITICAL)
        elif file_loglevel == 'ERROR':
            fh.setLevel(logging.ERROR)
        elif file_loglevel == 'WARNING':
            fh.setLevel(logging.WARNING)
        elif file_loglevel == 'DEBUG':
            fh.setLevel(logging.DEBUG)
        else: fh.setLevel(logging.INFO)

        log.addHandler(fh)

    return log

def convert_timestamp(timestamp):
    return time.ctime(float(timestamp)/1000000)