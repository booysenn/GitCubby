from gnupg import GPG
import base64

from . import GCLogger

from .state_manager import GCStateManager
from .constants import (
    ENCRYPTION_FINGERPRINT_FILE_PATH, GPG_COMPONENT_NAME, ENCRYPTION_KEY_MATERIAL, ENCRYPTION_PASSPHRASE,
    SIGN_FINGERPRINT_FILE_PATH, SIGN_KEY_MATERIAL, SIGN_PASSPHRASE
    ) 

gc_logger = GCLogger(__name__)
logger = gc_logger.get_logger()

class GCGpg():
    def __init__(self):
        self.state_manager = GCStateManager(GPG_COMPONENT_NAME)
        if not self.is_configured():
            self.first_run()

    def get_encryption_fingerprint(self, key_purpose='encryption'):
        """
        Get the GPG encryption key fingerprint
        
        Returns:
            str: The fingerprint, or None if not configured
        """
        if key_purpose == 'encryption':
            key_path = ENCRYPTION_FINGERPRINT_FILE_PATH
        elif key_purpose == 'signing':
            key_path = SIGN_FINGERPRINT_FILE_PATH
        else:
            raise ValueError(f"Invalid key purpose: {key_purpose}")
        
        if not key_path.exists():
            return None
        
        try:
            fingerprint = key_path.read_text().strip()
            logger.info(f"GPG key fingerprint: {fingerprint}")
            return fingerprint if fingerprint else None
        except Exception:
            return None

    def is_configured(self):
        """
        Check if GPG is configured
        
        Returns:
            bool: True if GPG key is configured
        """
        return self.state_manager.is_configured()
    
    def import_key(self, key_material, passphrase, ENCRYPTION_FINGERPRINT_FILE_PATH):
        gpg = GPG()
        decoded_key = base64.b64decode(key_material).decode('utf-8')
        import_result = gpg.import_keys(decoded_key, passphrase=passphrase)
        
        if import_result.fingerprints:
            fingerprint = import_result.fingerprints[0]
            gpg.trust_keys(fingerprint, 'TRUST_ULTIMATE')
            
            ENCRYPTION_FINGERPRINT_FILE_PATH.write_text(fingerprint)
            ENCRYPTION_FINGERPRINT_FILE_PATH.chmod(0o644)
            logger.info(f"GPG key imported with fingerprint: {fingerprint}")
        else:
            logger.error("Failed to import GPG key")
            raise Exception("GPG key import failed")

    def first_run(self):
            gpg = GPG()
            self.import_key(SIGN_KEY_MATERIAL, SIGN_PASSPHRASE, SIGN_FINGERPRINT_FILE_PATH)
            self.import_key(ENCRYPTION_KEY_MATERIAL, ENCRYPTION_PASSPHRASE, ENCRYPTION_FINGERPRINT_FILE_PATH)
            self.state_manager.mark_configured()
