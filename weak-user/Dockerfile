FROM ubuntu:14.04

RUN sed -i \
      -e 's|http://archive.ubuntu.com/ubuntu/|http://old-releases.ubuntu.com/ubuntu/|g' \
      -e 's|http://security.ubuntu.com/ubuntu/|http://old-releases.ubuntu.com/ubuntu/|g' \
      -e 's|http://[a-z][a-z].archive.ubuntu.com/ubuntu/|http://old-releases.ubuntu.com/ubuntu/|g' \
      /etc/apt/sources.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
       openssh-server \
       sudo \
       python3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

COPY generated/users.json /tmp/users.json
COPY scripts/create_users.py /tmp/create_users.py

RUN python3 /tmp/create_users.py /tmp/users.json \
    && rm -f /tmp/users.json /tmp/create_users.py

RUN printf '\nPasswordAuthentication yes\n\
PermitRootLogin no\n\
UsePAM no\n' >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]