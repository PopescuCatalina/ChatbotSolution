FROM rasa/rasa-sdk:3.5.1
COPY requirements.txt requirements.txt
USER root
RUN pip install -r requirements.txt

COPY ./actions /app/actions
VOLUME /app/actions