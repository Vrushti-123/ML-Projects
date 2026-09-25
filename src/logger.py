import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# LOG_FILE becomes: 09_19_2026_16_02_35.log
# Because you don't want every execution of your project to overwrite the previous log.
# for every log (everytime, time will be different) and new log_file will be created.

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
# this created --> C:\Users\Vrushti\MLProject\logs\09_19_2026_16_02_35.log
# a logs folder is created and new file is created every time inside it.

os.makedirs(logs_path,exist_ok=True)
# tries to create a directory with that entire path.
# "If the folder doesn't exist, create it. If it already exists, that's fine.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
# final location of the log file. 

logging.basicConfig(
    filename=LOG_FILE_PATH,
    # stores logs in this file.
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # 
    level=logging.INFO,
    # level=logging.INFO means:
    #  INFO, WARNING, ERROR, and CRITICAL messages are recorded, 
    # but DEBUG messages are not.
)
# %(asctime)s → Date and time when the log was generated.
# %(lineno)d → Line number where the logging call happened.
# %(name)s → Name of the logger.
# %(levelname)s → Severity/type of the log, such as INFO, WARNING, ERROR, CRITICAL, or DEBUG.
# %(message)s → The actual message written in the log, such as `logging.info("Training started")`.
