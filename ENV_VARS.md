# Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKUP_SCHEDULE` | `DAILY` | One of 15MIN DAILY HOURLY MONTHLY WEEKLY https://wiki.alpinelinux.org/wiki/Cron |
| `BACKUP_TARGET` | `file:///usr/local/backup` | A valid duplicity target, not all have been tested. https://duplicity.nongnu.org/vers7/duplicity.1.html#sect7 |
| `BACKUP_TIMEOUT_SECONDS` | `3600` | Timeout to prevent backup running indefinitely |
| `ENCRYPTION_KEY_MATERIAL` | `*Required*` | GPG key material use by backup encryption key |
| `ENCRYPTION_PASSPHRASE` | `*Required*` | PASSPHRASE used to decrypt backup encryption key |
| `EXTERNAL_HOSTNAME` | `localhost` | External hostname used to generate git clone urls |
| `EXTERNAL_HTTP_PORT` | `9980` | External http/s port used to generate git clone urls |
| `EXTERNAL_SSH_PORT` | `2222` | External ssh port used to generate git clone urls |
| `FORCE_RESTORE` | `False` | Forces a restore even if data loss would occur |
| `FULL_BACKUPS_TO_KEEP` | `4` | Number of full backups to keep by duplicity |
| `RESTORE_TIMEOUT_SECONDS` | `3600` | Timeout to prevent restore running indefinitely |
| `SIGN_KEY_MATERIAL` | `ENCRYPTION_KEY_MATERIAL` | GPG key material use by backup signing key |
| `SIGN_PASSPHRASE` | `ENCRYPTION_PASSPHRASE` | Passphrase used to decrypt backup signing key |
| `VERIFY_TIMEOUT_SECONDS` | `1800` | Timeout to prevent verify running indefinitely |
