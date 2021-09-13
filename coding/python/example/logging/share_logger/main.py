import mylib
import share_logging

logger = share_logging.get_logger(__name__)

# Main Code log information
logger.info('main info')
logger.debug('main debug')
logger.error('main error')

# call mylib function
mylib.do_something()

# Result
# [2020-12-30 11:21:12,092] main-><module> line:7 [INFO] main info
# [2020-12-30 11:21:12,093] main-><module> line:8 [DEBUG] main debug
# [2020-12-30 11:21:12,093] main-><module> line:9 [ERROR] main error
# [2020-12-30 11:21:12,093] mylib->do_something line:6 [INFO] Do Something !!!