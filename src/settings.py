from configparser import ConfigParser
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Setup ConfigParser to read in data from config file
config = ConfigParser()
config.read(os.path.join(__location__, 'config.conf'))

info_log_filename = config.get('GENERAL', 'info_log_filename')
warning_log_filename = config.get('GENERAL', 'warning_log_filename')
