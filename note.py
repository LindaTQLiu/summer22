'''ttq_git:
sgp_model/model_spline/model_XGB.py'''

# line 69
# create log folder
logdir = "log/"

log = setuplog(_modulename, cfg)

if dirExists(logdir):
    log.info("using existing log folder" + logdir)
else:
    if not createdir(logdir):
        log.critical("folder" + logdir + " not created. Exiting ...")
        sys.exit(2)
    else:
        log.info("folder " + logdir + " created. ")

# timestamp string
time_now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

import logging
'''
5 levels of severity of events:
- debug            logging.debug('debug msg')
- info             logging.info('info msg')
- warning          logging.warning('warning msg')
- error            logging.error('err msg')
- critical         logging.critical('critical msg')
only warning to critical are logged by default.

logging module provides a default logger.
'''
logger.setLevel(logging.INFO)   # to set from which level upwards (inclusive) start recording; if don't set, by default is warning level.

# basicConfig

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

''' written to a file named app.log:  root - ERROR - This will get logged to a file 
filemode: w -- each time basicConfig() is called, the log file is opened in "write mode" ; a -- append.
basicConfig() can only be called once. debug() ... critical() also call basicConfig(). So as long as basicConfig() is called somehow, can no longer configure the root logger.
default of basicConfig(): write to the console: ERROR:root:This is an error message
'''

# LogRecord
import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')   # log the process ID along with the level (of severity) and message.
logging.warning('This is a Warning')
 
shell>> 18472-WARNING-This is a Warning

https://docs.python.org/3/library/logging.html#logrecord-attributes    # list of LogRecord attributes.
[format] can take a string with LogRecord attributes in any arrangement.format

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')
 
shell>> 2018-07-11 20:12:06,288 - Admin logged in

# %(asctime)s adds the time of creation of the LogRecord.
# the [format] can be changed using the datefmt attribute, which uses the same formatting language as the formatting functions in the datetime module, such as time.strftime():
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('Admin logged out')
 
shell>> 12-Jul-18 20:53:19 - Admin logged out


# logging variable data
import logging
name = 'John'
logging.error('%s raised an error', name)
shell>> ERROR:root:John raised an error
---or---
import logging
name = 'John'
logging.error(f'{name} raised an error')     # f-strings: https://realpython.com/python-f-strings/
shell>> ERROR:root:John raised an error




