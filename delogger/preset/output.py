from logging import Logger

from delogger import Delogger
from delogger.decorator.debug_log import DebugLog
from delogger.preset.base import PresetsBase


class OutputPresets(PresetsBase):
    def make_logger(self, delogger: Delogger) -> Logger:
        delogger.load_modes(self.timed_rotating_filemode())
        delogger.load_decorators(DebugLog())

        slack_webhook_mode = self.slack_webhook_mode()
        if slack_webhook_mode:
            delogger.load_modes(slack_webhook_mode)

        return delogger.get_logger()


logger = OutputPresets("output_logger", is_queue=True).get_logger()
