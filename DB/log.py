import logging
import sys
# Local imports
import settings

info_log_filename = settings.info_log_filename
warning_log_filename = settings.warning_log_filename

# set up formatting
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] (%(process)d) %(module)s: %(message)s')

# set up logging to STDOUT for all levels INFO and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

# create logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.INFO)
mylogger.addHandler(sh)

# set up logging to a file for all levels INFO and higher
try:
    fh = logging.FileHandler(info_log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # create file logger object
    mylogger.addHandler(fh)
except IOError:
    print('It appears you are not on Linux, or do not have access to /var/log/ ...dropping file logging.')

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error
critical = mylogger.critical
