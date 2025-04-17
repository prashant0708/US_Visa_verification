import logging
import os

from datetime import datetime
from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

log_dir = 'logs'
log_path = os.path.join(from_root(),log_dir,LOG_FILE)
 
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    filename=log_path,
    filemode='w',
    format='[%(asctime)s] *** %(levelname)s*****%(name)s **** %(lineno)d ***** %(filename)s **** %(funcName)s  **** %(message)s',
    level=logging.INFO
)


