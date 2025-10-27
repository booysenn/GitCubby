import subprocess
from pathlib import Path
from . import GCGpg, GCLogger, GCStateManager
from .constants import (BACKUP_PATHS, BACKUP_COMPONENT_NAME, GPG_COMPONENT_NAME, FULL_BACKUPS_TO_KEEP, 
    PERIODIC_ROOT_PATH, PERIODIC_SCRIPT_NAME , PERIODIC_WANTED_BACKUP_SCRIPT_PATH, BACKUP_TARGET,
    BACKUP_SCHEDULE, RESTORE_TIMEOUT_SECONDS, BACKUP_TIMEOUT_SECONDS, VERIFY_TIMEOUT_SECONDS, FORCE_RESTORE)



gc_logger = GCLogger(__name__)
logger = gc_logger.get_logger()


class GCBackup():
    def __init__(self):
        self.backup_enabled = False
        if not GCStateManager(GPG_COMPONENT_NAME).is_configured():
            logger.error("GPG is not configured. Skipping backup.") # Might fall back to unencrypted backups
            return
        self.state_manager = GCStateManager(BACKUP_COMPONENT_NAME)
        self.restore_from_backup(FORCE_RESTORE)
        
        # Configure backup schedule on each start, allows changing schedule
        self.configure_backup_schedule()

        self.encrypt_key = GCGpg().get_encryption_fingerprint("encryption")
        self.sign_key = GCGpg().get_encryption_fingerprint("signing")

    def configure_backup_schedule(self):
        logger.info(f"Configuring backup schedule to {BACKUP_SCHEDULE.upper()}.")
        if (PERIODIC_WANTED_BACKUP_SCRIPT_PATH.exists()):
             logger.debug("Backup schedule already configured.")
             return

        for path in PERIODIC_ROOT_PATH.iterdir():
            script_link_path = path / PERIODIC_SCRIPT_NAME
            if script_link_path.exists(): script_link_path.unlink()
        try:
            PERIODIC_WANTED_BACKUP_SCRIPT_PATH.symlink_to('/usr/local/bin/backup')
            self.state_manager.mark_configured()
        except Exception as e:
            logger.exception(f"Failed to configure backup schedule: {e}")
            self.state_manager.mark_unconfigured()

    def is_path_empty(self, path):
        check_path = Path(path)
        try:
            if not check_path.exists():
                return True
            if check_path.is_dir():
                contents = list(check_path.iterdir())
                return len(contents) == 0
            elif check_path.is_file():
                return check_path.stat().st_size == 0
        except Exception as e:
            logger.exception(f"Error checking path: {e}")
            return False

    def restore_from_backup(self, force=False):
        logger.info(f"Attempting restore from backup")

        if any(not self.is_path_empty(path) for path in BACKUP_PATHS) or force:
            logger.warning("Date files/directories are not empty skipping restore")
            return

        cmd = [
            'duplicity',
            'restore',
            '--force',
            BACKUP_TARGET,
            '/'
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=RESTORE_TIMEOUT_SECONDS
            )
            
            if result.returncode == 0:
                logger.info("Restore completed successfully")
                if result.stdout:
                    logger.info(f"Restore details: {result.stdout}")
                return True
            else:
                logger.error("Restore failed")
                if result.stderr:
                    logger.error(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Restore timed out after {RESTORE_TIMEOUT_SECONDS} seconds")
            return False
        except Exception as e:
            logger.error(f"Restore failed with exception: {e}")
            return False

    def is_configured(self):
        """
        Check if Backup is configured
        
        Returns:
            bool: True if Backup is configured
        """
        return self.state_manager.is_configured()

    def first_run(self):
        try:
            logger.info("Initializing backup and auto restoring on first run")
            
            self.state_manager.mark_configured()
        except Exception as e:
            logger.error(f"Failed to initialize backup: {e}") # We do notfail on first run

    def perform_backup(self):
        logger.info("Starting backup.")
        include_args = []
        for backup_path in BACKUP_PATHS:
            include_args.extend(['--include', backup_path])

        cmd = [
            'duplicity',
            'incremental',
            '--full-if-older-than', '7D',
            '--sign-key', self.sign_key,
            '--encrypt-key', self.encrypt_key,
            '--allow-source-mismatch',
        ] + include_args + [
            '--exclude', '**',  # Exclude everything else
            '/',  # Source root
            BACKUP_TARGET  # Destination
        ]
    
        logger.debug(f"Running command (destination removed for security): {' '.join(cmd[:-1] )}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=BACKUP_TIMEOUT_SECONDS  # 1 hour timeout
            )
            
            if result.stdout:
                logger.info(f"Backup output:\n{result.stdout}")
            
            if result.returncode == 0:
                logger.info("Backup completed successfully")
                return True
            else:
                logger.error(f"Backup failed with exit code {result.returncode}")
                if result.stderr:
                    logger.error(f"Error output:\n{result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Backup timed out after 1 hour")
            return False
        except Exception as e:
            logger.error(f"Backup failed with exception: {e}")
            return False

    def cleanup_backups(self):
        """Remove old backups, keeping only the specified number of full backups"""
        logger.info(f"Cleaning up old backups, keeping {self.keep_full} full backups.")
        
        cmd = [
            'duplicity',
            'remove-all-but-n-full',
            str(FULL_BACKUPS_TO_KEEP),
            '--force',
            self.backup_target
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("Cleanup completed successfully")
                return True
            else:
                logger.error(f"Cleanup failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.exception(f"Cleanup failed with exception: {e}")
            return False

    def verify_backup(self):
        logger.info("Verifying backup.")
        
        cmd = [
            'duplicity',
            'verify',
            '--sign-key', self.sign_key,
            '--encrypt-key', self.encrypt_key,
            BACKUP_TARGET,
            'tmp/verify-test'
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=VERIFY_TIMEOUT_SECONDS
            )
            
            if result.returncode == 0:
                logger.info("Backup verification successful")
                return True
            else:
                logger.error(f"Backup verification failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.exception(f"Verification failed with exception: {e}")
            return False
