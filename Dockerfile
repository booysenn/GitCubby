FROM alpine:3.22.2

RUN set -eux; \
  apk add --no-cache \
    bash \
    openssh \
    git \
    yq-go \
    ncurses \
    git-daemon \
    lighttpd-mod_auth \
    lighttpd \
    apache2-utils \
    duplicity \
    keychain \
    py3-gitpython \
    py3-gnupg; \
    apk add --no-cache \
    py3-b2sdk \
    --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing

WORKDIR /srv/

COPY src/lighttpd.conf /etc/lighttpd/lighttpd.conf
COPY src/sshd_config /etc/ssh/sshd_config
COPY src/git-shell-commands /home/git/git-shell-commands
COPY /src/bin /usr/local/bin
COPY /src/utility /usr/local/bin/utility
COPY /src/shell_utility /usr/local/bin/shell_utility

# Create git group and user, add git to lighttpd group
RUN addgroup -S git && \
    adduser -D -h /home/git -s /usr/bin/git-shell -G git git && \
    passwd -u git && \
    mkdir -p /home/git/.ssh && \
    chmod 700 /home/git/.ssh && \
    touch /home/git/.ssh/authorized_keys && \
    chmod 600 /home/git/.ssh/authorized_keys && \
    chown -R git:git /home/git/.ssh && \
    touch /etc/lighttpd-htdigest.user && \
    chown -R git:git /etc/lighttpd-htdigest.user && \
    chmod 640 /etc/lighttpd-htdigest.user && \
    mkdir -p /private && \
    mkdir -p /public && \
    chown -R git:git /private /public && \
    chmod 2775 /private /public && \
    mkdir -p /var/log/ssh /var/log/git && \
    touch /var/log/ssh/auth.log && \
    touch /var/log/git/access.log && \
    chown -R git:git /var/log/git && \
    chmod 755 /var/log/ssh /var/log/git && \
    chmod 666 /var/log/ssh/auth.log /var/log/git/access.log && \
    ln -s /usr/local/bin/shell_utility /home/git/git-shell-commands/utility

RUN echo -n "" > /etc/motd

EXPOSE 22
EXPOSE 80

ENTRYPOINT ["/usr/local/bin/entrypoint.py"]
