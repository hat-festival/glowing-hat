FROM python:3.9 

ENV PROJECT hatlights
ENV PLATFORM docker
WORKDIR /opt/${PROJECT}

RUN apt-get update && apt-get install -y redis rsync

COPY ./ /opt/${PROJECT}
COPY docker-config/bashrc /root/.bashrc

RUN python -m pip install --upgrade pip
RUN python -m pip install --ignore-installed -r requirements-dev.txt

COPY ./docker-config/entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]
