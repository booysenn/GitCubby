# GitCubby

## Introduction

The goal of this project is to create a easy to launch and run git server container. This server is not meant ot be full featured like projects like forgejo but easy to launch and configure through environment variables and config files requiring no ui configuration.

## Features

Access over HTTP for authenitcate push and pull as well as unauthenticated pull for selected repositories. Authencticated SSH push and pull for all repositories. Simple backup and recovery process built on duplicity. BAsic git-shell setup to manage the platform.

## Limitations

This will not support clear multiuser environments. There is limited user seperation but users are not intended to setup their own repos and there are simply public and private repos. Public repos have unautheticated http pull allowing for use in local automations easily without needed complex key management. Push access is authenticated on all repos. This does mean that more sensitive projects can be kept locally authenticated, but that all users who have user accounts/ssh keys to the system can access all repos  (no user segregation).

## Deployment




## Environment Variables

<!-- ENV_VARS_START -->
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
<!-- ENV_VARS_END -->