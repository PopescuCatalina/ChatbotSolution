FROM rasa/rasa-sdk:3.5.1
COPY requirements.txt requirements.txt
USER root
RUN pip install -r requirements.txt
#
#WORKDIR /app
#RUN chgrp -R 0 /app && chmod -R g=u /app
#USER 1001
#
## Create a volume for temporary data
#VOLUME /tmp
#
## change shell
#SHELL ["/bin/bash", "-o", "pipefail", "-c"]
#
## the entry point
#EXPOSE 5005
#ENTRYPOINT ["rasa"]
#CMD ["--help"]