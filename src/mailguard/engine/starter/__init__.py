import logging

from mailguard.runner.chief import MainRunner
from mailguard.tasks.services import tasks

logger = logging.getLogger(__name__)

# TODO: need to check if it works this way
logger.info("start job runner")
runner = MainRunner(tasks)
runner.run()
