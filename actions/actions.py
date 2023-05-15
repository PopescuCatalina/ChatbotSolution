# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from datetime import datetime


class ActionReadJSON(Action):
        def name(self) -> Text:
            return "action_hello_json"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            jsonFile = open('./actions/BusinessProfile.json', 'r')
            values = json.load(jsonFile)
            idValue = values['data']['businessName']
            dispatcher.utter_message(
                text=("\U0001F916 Hello, I'm " + str(idValue) + " Chatbot, and I'm here to help you with your inquiries!"))
            return []


class ActionReadHours(Action):
    def name(self) -> Text:
        return "action_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        jsonFile = open('./actions/BusinessProfile.json',
                        'r')
        values = json.load(jsonFile)
        concat = ' '
        for criteria in values['data']['workingHours']:
            if values['data']['workingHours'][criteria]['isClosed'] is False:
                date_start = datetime.strptime(values['data']['workingHours'][criteria]['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
                start = date_start.strftime('%H:%M:%S')
                date_end = datetime.strptime(values['data']['workingHours'][criteria]['end'], '%Y-%m-%dT%H:%M:%S.%fZ')
                end = date_end.strftime('%H:%M:%S')
                sent = ' ' + str(criteria) + ' from ' + str(start) + ' to ' + str(end)
                concat += sent
            else:
                sent = ' ' + str(criteria) + ' is closed'
                concat += sent
        dispatcher.utter_message(text=("\U0001F916 Here are the hours of operation, " + concat))
        return []

class ActionReadRates(Action):
    def name(self) -> Text:
        return "action_rates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        jsonFile = open('./actions/BusinessProfile.json',
                        'r')
        values = json.load(jsonFile)
        final = ''
        category = set()
        for criteria in values['data']['services']:
            element = str(criteria['category'])
            category.add(element)

        for i in category:
            sent = "For category " + i + " we have the following services"
            concat = ''
            for criteria in values['data']['services']:
                if criteria['category'] == i:
                    concat += ", Service " + str(criteria['name']) + " : " + str(criteria['price']) + str(
                        criteria['currency'])
            final += sent + concat + "\n\n"

        dispatcher.utter_message(text=("\U0001F916" + final))
        return []

class ActionReadServices(Action):
    def name(self) -> Text:
        return "action_services"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        jsonFile = open('./actions/BusinessProfile.json',
                        'r')
        values = json.load(jsonFile)
        final = ''
        category = set()
        for criteria in values['data']['services']:
            element = str(criteria['category'])
            category.add(element)

        for i in category:
            sent = "For category " + i + " we have the following services"
            concat = ''
            for criteria in values['data']['services']:
                if criteria['category'] == i:
                    concat += ", Service " + str(criteria['name'])
            final += sent + concat + "\n\n"

        dispatcher.utter_message(text=("\U0001F916 Here are our service categories, " + final))
        return []
#
class ActionRedirectToHuman(Action):
    def name(self) -> Text:
        return "action_redirect_to_human"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=("Ok, you will be redirected to a humanoid colleague! See you!"))
        return []

class ActionReadDuration(Action):
    def name(self) -> Text:
        return "action_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        jsonFile = open('./actions/BusinessProfile.json',
                        'r')
        values = json.load(jsonFile)
        final = ' '
        for criteria in values['data']['services']:
            sent = []
            for i in criteria['duration']:
                sent.append(i)
            if len(sent) == 2:
                for x in range(1):
                    concat = str(criteria['name']) + " duration " + str(
                        criteria['duration']['hours']) + " hours" + " and " + str(
                        criteria['duration']['minutes']) + " minutes"
            else:
                if sent[0] == 'minutes':
                    concat = str(criteria['name']) + " duration " + str(criteria['duration']['minutes']) + " minutes"
                if sent[0] == 'hours':
                    concat = str(criteria['name']) + " duration " + str(criteria['duration']['hours']) + " hours"
            final += concat + "\n\n"

        dispatcher.utter_message(text=("\U0001F916 Here are our service duration, " + final))
        return []