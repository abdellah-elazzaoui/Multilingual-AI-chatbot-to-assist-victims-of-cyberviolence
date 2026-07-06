import logging
from datetime import datetime
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_response(message:str) -> dict:
    "Format Response message"
    return {
        "message":message,
        "timestamp":datetime
    } 