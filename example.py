import sys, os
from PrintLogger import PrintLogger as plog


# Setting
if not os.path.isdir("./logs"):
    os.mkdir("./logs")

plog.set_logger("NOTSET", "./logs/log.log")

# If you want to set rich Handler
sys.excepthook = plog.handle_exception

# If you want to output only debug level and above
plog.set_logger("DEBUG", "./logs/log.log")

# If you want a file rotation every midnight
plog.set_logger("INFO", "./logs/log.log", logging_type="time")

# If you want to set the global timezone
plog.set_logger("ERROR", "./logs/log.log", logging_type="time", tz="Asia/Seoul")

# If you want to change only the log format time zone
plog.set_logger("WARNING", ".\\logs\\log.log", logging_type="time", formatter_tz="Asia/Seoul")

# Use
plog.exception("This is exception level")
plog.critical("This is critical level")
plog.error("This is error level")
plog.warning("This is warning level")
plog.info("This is info level")
plog.debug("This is debug level")
# plog.log("This is log level", "This is log message")
plog.log(20, "This is log message")
plog.log("DEBUG", "This is log message")

