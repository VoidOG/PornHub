import pytz
import sys
import logging
import platform
from importlib import import_module
from datetime import datetime, timezone

from PornHub.bot import PornHub
from PornHub.plugins import loadModule
from pyrogram import idle
from asyncio import get_event_loop_policy
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = "PhLogs.txt"
timezone = pytz.timezone('Asia/Jakarta')

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt=datetime.now(timezone).strftime("%d - %b - %y | %H:%M:%S"),
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.crypto.aes").setLevel(logging.INFO)
logging.getLogger("pyrogram.session.session").setLevel(logging.INFO)
logging.getLogger("pyrogram.connection.connection").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    for mod in loadModule():
        import_module(f"PornHub.plugins.{mod}")
    pornhub = PornHub()

    try:
        await pornhub.start()

        if "test" not in sys.argv:
            await idle()
    except KeyboardInterrupt:
        logger.warning("Forced stop, Bye!")
    finally:
        await pornhub.stop()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
