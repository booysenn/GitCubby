import subprocess

from . import GCLogger

from . import GCStateManager
from .constants import KEYS_DIR_PATH , AUTHORIZED_KEYS_PATH, SSH_COMPONENT_NAME

gc_logger = GCLogger(__name__)
logger = gc_logger.get_logger()

class GCSsh():
    def __init__(self):
        self.state_manager = GCStateManager(SSH_COMPONENT_NAME)
        if not self.is_configured():
            self.first_run()

    def is_configured(self):
        """
        Check if GPG is configured
        
        Returns:
            bool: True if GPG key is configured
        """
        return self.state_manager.is_configured()

    def first_run(self):
        logger.info("Generating SSH host keys")
        subprocess.run(['ssh-keygen', '-A'], check=True) # Generate SSH host keys
        self.state_manager.mark_configured()

    def install_ssh_keys(self):
        keys_dir = KEYS_DIR_PATH
        authorized_keys = AUTHORIZED_KEYS_PATH
        logger.info(f"Installing SSH keys from {str(keys_dir)} to {str(authorized_keys)}")
        with open(authorized_keys, 'w') as ak:
            for key_file in keys_dir.glob('*.pub'):
                username = key_file.stem  # filename without .pub extension
                logger.info(f"Installing SSH key for user {username}")
                key_content = key_file.read_text().strip()
                ak.write(f'environment="GIT_USER={username}",no-port-forwarding,no-X11-forwarding,no-agent-forwarding {key_content}\n')