# Pinger Smart Autoreply Bot
#### This repository contains the main skeleton of the Smart Autoreply AI bot.
## Setup
### Make sure to clone the project and install docker images and containers from docker-compose.yml

```bash
git clone <project_name>
cd <project_name>
```
### Increase the RAM at 6GB for docker containers (I had problems with only 4GB)
### Build the docker “pinger_requirements” image by running:
```docker build -t pinger_requirements -f Dockerfile .```
### (Don’t forget to add the dot (.) at the end. It’s important!)
### Then create the containers by running
```docker compose up```

### After that, you can go to the index2.html file in your own browser and chat with your own bot.


### For those of you who do not have an Intel processor on your computer, you must change the structure in the docker-compose.yml file as follows.

```bash
  rasa-pinger:
    image: khalosa/rasa-aarch64:3.5.2
    networks: ['rasa-project2']
    ports:
    - "5005:5005"
    volumes:
    - "./:/app/"
    command:
      - run
      - -vv
      - --enable-api
      - --cors
      - '*'
```

