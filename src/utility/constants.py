from pathlib import Path
from .common import get_env_stripped
from os import environ


STATE_PATH = Path("/etc/gitcubby/")

ENCRYPTION_FINGERPRINT_FILE_PATH = STATE_PATH / 'encryption_fingerprint'
SIGN_FINGERPRINT_FILE_PATH = STATE_PATH / 'signing_fingerprint'

BACKUP_PATHS = [
    '/private',
    '/public',
    '/etc/lighttpd-htdigest.user'
]

# External hostname used to generate git clone urls
EXTERNAL_HOSTNAME = get_env_stripped('EXTERNAL_HOSTNAME', 'localhost')
# External ssh port used to generate git clone urls
EXTERNAL_SSH_PORT = get_env_stripped('EXTERNAL_SSH_PORT', 2222, cast=int)
# External http/s port used to generate git clone urls
EXTERNAL_HTTP_PORT = get_env_stripped('EXTERNAL_HTTP_PORT', 9980, cast=int) 

# GPG key material use by backup encryption key
ENCRYPTION_KEY_MATERIAL = get_env_stripped('ENCRYPTION_KEY_MATERIAL', required=True)
# PASSPHRASE used to decrypt backup encryption key
ENCRYPTION_PASSPHRASE = get_env_stripped('ENCRYPTION_PASSPHRASE', required=True)
environ['PASSPHRASE'] = ENCRYPTION_PASSPHRASE

# GPG key material use by backup signing key
SIGN_KEY_MATERIAL = get_env_stripped('SIGN_KEY_MATERIAL', ENCRYPTION_KEY_MATERIAL)
# Passphrase used to decrypt backup signing key
SIGN_PASSPHRASE = get_env_stripped('SIGN_PASSPHRASE', ENCRYPTION_PASSPHRASE)
environ['SIGN_PASSPHRASE'] = SIGN_PASSPHRASE

# Number of full backups to keep by duplicity
FULL_BACKUPS_TO_KEEP = get_env_stripped('FULL_BACKUPS_TO_KEEP', 4, cast=int)

# One of 15MIN DAILY HOURLY MONTHLY WEEKLY https://wiki.alpinelinux.org/wiki/Cron
BACKUP_SCHEDULE = get_env_stripped('BACKUP_SCHEDULE', 'DAILY')
ALLOWED_BACKUP_SCHEDULE_VALUES = ["15MIN", "DAILY", "HOURLY", "MONTHLY", "WEEKLY"]
if (BACKUP_SCHEDULE not in ALLOWED_BACKUP_SCHEDULE_VALUES):
    BACKUP_SCHEDULE = 'DAILY'

PERIODIC_ROOT_PATH = Path('/etc/periodic')

PERIODIC_SCRIPT_NAME = 'backup'

PERIODIC_WANTED_BACKUP_SCRIPT_PATH = Path('/etc/periodic') / BACKUP_SCHEDULE.lower() / PERIODIC_SCRIPT_NAME

# A valid duplicity target, not all have been tested. https://duplicity.nongnu.org/vers7/duplicity.1.html#sect7
BACKUP_TARGET = get_env_stripped('BACKUP_TARGET', "file:///usr/local/backup")
# Timeout to prevent restore running indefinitely
RESTORE_TIMEOUT_SECONDS = get_env_stripped('RESTORE_TIMEOUT_SECONDS', 3600, cast=int)
# Timeout to prevent backup running indefinitely
BACKUP_TIMEOUT_SECONDS = get_env_stripped('BACKUP_TIMEOUT_SECONDS', 3600, cast=int)
# Timeout to prevent verify running indefinitely
VERIFY_TIMEOUT_SECONDS = get_env_stripped('VERIFY_TIMEOUT_SECONDS', 1800, cast=int)

# Forces a restore even if data loss would occur
FORCE_RESTORE = get_env_stripped('FORCE_RESTORE', False, cast=bool)

LOG_FILE_PATH = Path('/var/log/gitcubby/main.log')
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

KEYS_DIR_PATH = Path('/keys')
AUTHORIZED_KEYS_PATH = Path('/home/git/.ssh/authorized_keys')

SSH_COMPONENT_NAME = 'ssh'
GPG_COMPONENT_NAME = 'gpg'
BACKUP_COMPONENT_NAME = 'backup'