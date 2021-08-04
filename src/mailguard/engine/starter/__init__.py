import logging

from mailguard.tasks.services import tasks
from mailguard.runner.chief import MainRunner

logger = logging.getLogger(__name__)

# TODO: need to check if it works this way
logger.info('start job runner')
runner = MainRunner(tasks)
runner.run()
