#!/usr/bin/env python3

import os
import subprocess

from utility import GCLogger, GCGpg, GCSsh, GCBackup


logger = GCLogger(__name__).get_logger()
logger.info("Starting GitCubby")

logger.info("Initializing SSH Server and keys")
ssh = GCSsh()
ssh.install_ssh_keys()

logger.info("Initializing GPG Backup Keys")
gpg = GCGpg()

logger.info("Initializing Duplicity Backup")
backup = GCBackup()
if backup.is_configured():
    subprocess.Popen(['crond'])

subprocess.Popen([
    '/usr/sbin/lighttpd', '-D', '-f', '/etc/lighttpd/lighttpd.conf'
])

if ssh.is_configured():
    os.execv("/usr/sbin/sshd", ["/usr/sbin/sshd", "-D"])
