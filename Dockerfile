#
# Docker image that can be run under Marathon management to dynamically scale a Marathon service running on DC/OS.
#

FROM centos:7

ARG STRICTUSER_UID=99
ARG STRICTUSER_GID=99
ARG STRICTUSER_USER=nobody
ARG STRICTUSER_GROUP=nobody
ARG DATA_FOLDER='/marathon-autoscale'

RUN grep nobody /etc/passwd && ls -l /home && id

RUN [[ "$STRICTUSER_UID" != '99' && "$STRICTUSER_GID" != '99' ]] && \
    usermod -o -u $STRICTUSER_UID nobody && \
    groupmod -o -g $STRICTUSER_GID nobody || true

# Copy the python scripts into the working directory
WORKDIR $DATA_FOLDER

ADD / $DATA_FOLDER

RUN yum -y install epel-release \
    && yum -y install make gcc g++ openssl-devel python36 python36-pip python36-devel python36-libs \
    && yum clean all

RUN pip3 install -r requirements.txt

RUN chown -R nobody:nobody $DATA_FOLDER

# Start the autoscale application
CMD python3 marathon_autoscaler.py
