FROM ruby:2

WORKDIR /opt

RUN gem install nineteen-eighty-two

COPY script.sh /opt

# RUN chmod +x /opt/script.sh
ENTRYPOINT ["bash", "/opt/script.sh"]
