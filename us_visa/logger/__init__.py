import logging
import os

from datetime import datetime
from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

log_dir = 'logs'
# log_path = os.path.join(from_root(),log_dir,LOG_FILE)
 
# os.makedirs(log_dir,exist_ok=True)
log_dir = os.path.join(from_root(), "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, LOG_FILE)

# Clear previous handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    format='[%(asctime)s] *** [levelname: %(levelname)s]  **** [Line number: %(lineno)d] ***** [File name: %(filename)s] ***** [Function name : %(funcName)s]  **** [%(message)s]',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()  # Also prints to console
    ]
)


