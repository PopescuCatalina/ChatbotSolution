




https://github.com/PopescuCatalina/ChatbotSolution/assets/43966104/a098a993-71ab-440c-bf16-8840ccdc33bb


#  Smart Autoreply Bot
 This repository contains the main skeleton of the Smart Autoreply AI bot.
## Setup
 Make sure to clone the project and install docker images and containers from docker-compose.yml

```bash
git clone <project_name>
cd <project_name>
```

(OPTIONAL) Increase the RAM at 6GB for docker containers (I had problems with only 4GB)
Build the docker “pinger_requirements” image by running:
```docker build -t pinger_requirements -f Dockerfile .```

(Don’t forget to add the dot (.) at the end. It’s important!)

Then create the containers by running
```docker compose up```

After that, you can go to the index2.html file in your own browser and chat with your own bot.


For those of you who do not have an Intel processor on your computer, you must change the structure in the docker-compose.yml file as follows.

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

## Business Profile - Local vs API Endpoint 
For an up-to-date profile we must:
- have `autoreplay-api` app started
- make sure that `actions/actions.py` has this set to false (or 0):

```
USE_LOCAL_BP = 0
```

If you don't want to bother setting up other apps you can set the `USE_LOCAL_BP` to "1" but the business profile may not be up to date.
