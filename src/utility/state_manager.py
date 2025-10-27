from pathlib import Path

from .constants import STATE_PATH
from .logger import GCLogger

logger = GCLogger(__name__).get_logger()

class GCStateManager:
    def __init__(self, featureName):
        self.featureName = featureName
        self.state_file = STATE_PATH / featureName
        self.create_first_run_path()

    
    def is_configured(self):
        if Path(self.state_file).exists():
            logger.info(f"Already configured, path {self.state_file} exists")
            return True
        return False

    def create_first_run_path(self):
        if not Path(STATE_PATH).exists():
            logger.info("Creating state directory")
            Path(STATE_PATH).mkdir(parents=True, exist_ok=True)

    def mark_configured(self):
            state_file = self.state_file
            Path(state_file).touch()

    def mark_unconfigured(self):
            state_file = self.state_file
            Path(state_file).unlink()