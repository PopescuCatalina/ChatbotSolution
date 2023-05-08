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

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello, I'm [Business Name] Chatbot, and I'm here to help you with your inquiries!")

        return []

class ActionReadJSON(Action):
        def name(self) -> Text:
            return "action_hello_json"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            jsonFile = open('./actions/BusinessProfile.json', 'r')
            values = json.load(jsonFile)
            idValue = values['business_name']
            dispatcher.utter_message(text=("Hello, I'm " + str(idValue) + " Chatbot, and I'm here to help you with your inquiries!" ))
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
        dispatcher.utter_message(text=("Here are the hours of operation!"))
        for criteria in values['hours']:
                 dispatcher.utter_message(text=(str(criteria) + " : " + values['hours'][criteria]))
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
        dispatcher.utter_message(text=("Here are the rates of services!"))
        for criteria in values['services']:
                 dispatcher.utter_message(text=(criteria["name"] + " : " + criteria["price"]))
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
        dispatcher.utter_message(text=("Here are services!"))
        for criteria in values['services']:
                 dispatcher.utter_message(text=(criteria["name"] + " : " + criteria["description"]))
        return []

class ActionRedirectToHuman(Action):
    def name(self) -> Text:
        return "action_redirect_to_human"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=("Ok, you will be redirected to a humanoid colleague! See you!"))
        return []