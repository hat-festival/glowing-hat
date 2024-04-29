FROM python:3.11

ARG PROJECT
ENV PLATFORM docker
WORKDIR /opt/${PROJECT}

RUN apt-get update && apt-get install -y redis rsync libgl1

COPY ./ /opt/${PROJECT}
COPY docker-config/bashrc /root/.bashrc

RUN python -m pip install --upgrade pip
RUN python -m pip install --ignore-installed -r dev-requirements.txt

COPY ./docker-config/entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]
