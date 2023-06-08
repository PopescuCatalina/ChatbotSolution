# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
from typing import Any, Text, Dict, List

import rasa_sdk.events
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
from datetime import datetime
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from rasa_sdk.events import ActionReverted
from collections import OrderedDict

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
                text=("\U0001F916 Hello, I'm " + str(idValue) + " Chatbot, and I'm here to help you with bookings or any information you may need."))
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
        entity1 = tracker.get_slot("entity1")
        #rate = tracker.get_slot("rate")
        similar = 0
        if entity1 != None:
            for criteria in values['data']['services']:
                if criteria['name'] == entity1:
                    similar = 1
                    dispatcher.utter_message(
                        text=(f"\U0001F916 The price for the {entity1} is " + str(
                            criteria['price']) + " " + str(criteria['currency'])))
                    slot_value = None
                    return [SlotSet("rate", slot_value)]
                    #return [SlotSet("entity1", slot_value)]

            if similar == 0:
                return [rasa_sdk.events.FollowupAction("action_service_category_2")]
        else:
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

        #dispatcher.utter_message(text=("\U0001F916 Nu exista rate"))
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
        cat_hairstyling = set()
        cat_barber = set()
        for criteria in values['data']['services']:
            element = criteria['category']
            if element == 'Hairstyling':
                cat_hairstyling.add(criteria['name'])
            elif element == 'Barbershop':
                cat_barber.add(criteria['name'])
        # sent = "At this moment we have a selection of "+ str(len(category))+" categories of services available: "
        # for i in category:
        #     final += i + ", "

        sent = " We offer a wide range of services ranging from " + ", ".join(cat_hairstyling) + \
            " to " +  ", ".join(cat_barber) + "."
        dispatcher.utter_message(text=("\U0001F916" + sent + " Is there something specific you are interested in?"))
        return []
#
class ActionRedirectToHuman(Action):
    def name(self) -> Text:
        return "action_redirect_to_human"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text=("Ok, you will be redirected to a humanoid colleague! See you!"))
        dispatcher.utter_message(text=("I've sent them a notification. In the meantime, I can help you with other information."))
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
        entity1 = tracker.get_slot("entity1")
        time = tracker.get_slot("time")
        final = ' '
        #if time != None:
        if entity1 != None:
            for criteria in values['data']['services']:
                if criteria['name'] == entity1:
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
                            concat = str(criteria['name']) + " duration " + str(
                                criteria['duration']['minutes']) + " minutes"
                        if sent[0] == 'hours':
                            concat = str(criteria['name']) + " duration " + str(
                                criteria['duration']['hours']) + " hours"

                    final += concat + "\n\n"
                    dispatcher.utter_message(
                        text=(f"\U0001F916 The {str(criteria['name'])} service is " + final))
                    slot_value = None
                    return [SlotSet("time", slot_value)]
                    #return [SlotSet("entity1", slot_value)]

            if final == ' ':
                return [rasa_sdk.events.FollowupAction("action_service_category_2")]


        else:
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

        #dispatcher.utter_message(text=("\U0001F916 Nu exista duration"))
        return []

class ActionServicecategory2(Action):
    def name(self) -> Text:
        return "action_service_category_2"

    def similar(self, a, b) -> float:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Compute embedding for both lists
        embedding_1 = model.encode(a, convert_to_tensor=True)
        embedding_2 = model.encode(b, convert_to_tensor=True)
        return float((util.pytorch_cos_sim(embedding_1, embedding_2)))

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entity1 = tracker.get_slot("entity1")
        time = tracker.get_slot("time")
        rate = tracker.get_slot("rate")
        booking = tracker.get_slot("booking")
        availability = tracker.get_slot("availability")
        timeline_date = tracker.get_slot("timeline_date")
        timeline_time = tracker.get_slot("timeline_time")
        jsonFile = open('./actions/BusinessProfile.json',
                       'r')
        values = json.load(jsonFile)
        concat = ''
        sim = []
        name = []
        description = []
        price = []
        currency = []
        category_found=0
        similarity_max = 0
        if entity1 != None:
            for criteria in values['data']['services']:
                similarity = self.similar(criteria['name'], entity1)
                if similarity > 0.5:
                    name.append(criteria['name'])
                    sim.append(similarity)
                    description.append(criteria['description'])
                    price.append(criteria['price'])
                    currency.append(criteria['currency'])


            dataset = pd.DataFrame({'Name': name, 'Similarity': sim, 'Description':description , 'Price': price, 'Currency':currency })
            sorted_dataset = dataset.sort_values('Similarity', ascending=False)
            for index, row in sorted_dataset.iterrows():
                if row['Similarity'] >= 0.7:
                    category_found += 1
                    if row['Similarity'] >= 0.98:
                      similarity_max = 1
                      ful_sim = str(row['Description'])
                    #   dispatcher.utter_message(text=(f"\U0001F916 Awesome, we have {str(row['Name'])} which describe: " + ful_sim))
                      dispatcher.utter_message(text=(f"\U0001F916 Yes, we offer {str(row['Name'])} service: " + ful_sim))
                      if time != None and similarity_max == 1:
                          return [rasa_sdk.events.FollowupAction("action_duration")]
                      if rate != None and similarity_max == 1:
                          return [rasa_sdk.events.FollowupAction("action_rates")]
                      # if availability != None and similarity_max == 1:
                      #   if timeline_date != None and timeline_time != None:
                      #        return [rasa_sdk.events.FollowupAction("availability_for_book_action")]
                      #   else:
                      #       dispatcher.utter_message(text=(f"\U0001F916 Please rephrase and tell us a time slot for availability checking !"))
                      # if booking != None and similarity_max == 1:
                      #   if timeline_date != None and timeline_time != None:
                      #        return [rasa_sdk.events.FollowupAction("booking_slots_action")]
                      #   else:
                      #       dispatcher.utter_message(text=(f"\U0001F916 Please rephrase and tell us a time slot for booking a slot!"))
                      if availability != None :
                            return [rasa_sdk.events.FollowupAction("availability_for_book_action")]
                      if booking != None :
                            return [rasa_sdk.events.FollowupAction("booking_slots_action")]
                    else:
                      concat += " Service " + str(row['Name'])

                # if there is an element with the similarity score less than 0.7 and category_found = 0 then in this case we don't have another fit and it is a unique match
                if row['Similarity'] <= 0.7 and category_found == 0:
                    category_found += 1
                    concat += " Service " + str(row['Name'])
            concat += " \n .Which service are you interested in?"

            if similarity_max == 0:
                if category_found >= 1:
                    dispatcher.utter_message(text=(f"\U0001F916 Here are our services similar to your requirement of {entity1} : " + concat))
                else:
                    # dispatcher.utter_message(text=(f"\U0001F916 I can't find any information about the service {entity1} "))
                    dispatcher.utter_message(text=(f"\U0001F916 Sorry. But I don't know how to answer that. \
                                                   I have information about common services and rates and can help you book an appointment. \
                                                   Can you rephrase your question?"))

        return []

class ActionAvailabilityforBooking(Action):
    def name(self) -> Text:
        return "availability_for_book_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity1 = tracker.get_slot("entity1")
        timeline_date = tracker.get_slot("timeline_date")
        timeline_time = tracker.get_slot("timeline_time")
        dates = ''
        times = ''
        if timeline_time != None and timeline_date != None:
            for date in timeline_date:
                dates += str(date) + " "
            for time in timeline_time:
                times += str(time) + " "
            if entity1 != None:
                dispatcher.utter_message(text=(f"\U0001F916 Do you want to check the availability for {entity1} in {dates} at {times} ?"))
            else:
                dispatcher.utter_message(text=(f"\U0001F916 Please provide us a service for availability checking !"))
                return [rasa_sdk.events.FollowupAction("action_service_category_2")]
        else:
            return [rasa_sdk.events.FollowupAction("action_service_category_2")]

        return []


class ActionBookingSlots(Action):
    def name(self) -> Text:
        return "booking_slots_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity1 = tracker.get_slot("entity1")
        timeline_date = tracker.get_slot("timeline_date")
        timeline_time = tracker.get_slot("timeline_time")
        dates = ''
        times = ''
        if timeline_time != None and timeline_date != None:
            for date in timeline_date:
                dates += str(date) + " "
            for time in timeline_time:
                times += str(time) + " "
            if entity1 != None:
                dispatcher.utter_message(text=(f"\U0001F916 Do you want to book a slot for {entity1} in {dates} at {times}?"))
            else:
                dispatcher.utter_message(text=(f"\U0001F916 Please provide us a service for booking!"))
                return [rasa_sdk.events.FollowupAction("action_service_category_2")]
        else:
            return [rasa_sdk.events.FollowupAction("action_service_category_2")]
        return []

class ActionBookingSlotsYes(Action):
    def name(self) -> Text:
        return "booking_slots_yes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity1 = tracker.get_slot("entity1")
        timeline_date = tracker.get_slot("timeline_date")
        timeline_time = tracker.get_slot("timeline_time")
        dates = ''
        times = ''
        if timeline_time != None and timeline_date != None:
            for date in timeline_date:
                dates += str(date) + " "
            for time in timeline_time:
                times += str(time) + " "
            if entity1 != None:
                dispatcher.utter_message(text=(f"\U0001F916 We are glad that you want to reserve a slot for {entity1} in {dates} at {times}"))
                slot_value = None
                return [SlotSet("booking", slot_value)]
            else:
                return [rasa_sdk.events.FollowupAction("action_service_category_2")]
        return []

class ActionBookingSlotsNo(Action):
    def name(self) -> Text:
        return "booking_slots_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=(f"\U0001F916 We are sorry that you do not want to reserve a slot"))
        return []

class ActionAvailabilityforBookingYes(Action):
    def name(self) -> Text:
        return "availability_for_book_yes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity1 = tracker.get_slot("entity1")
        timeline_date = tracker.get_slot("timeline_date")
        timeline_time = tracker.get_slot("timeline_time")
        dates = ''
        times = ''
        for date in timeline_date:
            dates += str(date) + " "
        for time in timeline_time:
            times += str(time) + " "

        jsonFile = open('./actions/BusinessProfile.json',
                        'r')
        values = json.load(jsonFile)
        final = ' '
        if entity1 != None:
            for criteria in values['data']['services']:
                if criteria['name'] == entity1:
                    sent = []
                    for i in criteria['duration']:
                        sent.append(i)
                    if len(sent) == 2:
                        for x in range(1):
                            concat = str(criteria['duration']['hours']) + " hours" + " and " + str(criteria['duration']['minutes']) + " minutes"
                    else:
                        if sent[0] == 'minutes':
                            concat = str(criteria['duration']['minutes']) + " minutes"
                        if sent[0] == 'hours':
                            concat = str(criteria['duration']['hours']) + " hours"

                    final += concat + "\n\n"

            dispatcher.utter_message(text=(f"\U0001F916 We are glad that you want to check the availability for the service {entity1} that lasts {final} in {dates} at {times} "))
            slot_value = None
            return [SlotSet("availability", slot_value)]
        else:
            dispatcher.utter_message(text=(f"\U0001F916 Please provide us a service for booking!"))
            return [rasa_sdk.events.FollowupAction("action_service_category_2")]

        return []

class ActionAvailabilityforBookingNo(Action):
    def name(self) -> Text:
        return "availability_for_book_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=(f"\U0001F916 We are sorry that you do not want to check the availability for a slot"))
        return []