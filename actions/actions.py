# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "%s ભાષા %s પરિવાર ની છે.\n તેની જીનસ %s છે.\n તેનો આઇ.એસ.ઓ. કોડ %s છે." % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "માફ કરશો! અમારી પાસે %s ભાષા માટે વિગતો નથી." % query_lang)

        return []

class Actionfeedback(Action):

    def name(self) -> Text:
        return "feedback" 
    def run(self, dispatcher, tracker,domain):
        dispatcher.utter_message(text = "શું મારી મદદ થી તમને સંતોષ થયો?")
        # feed = input()
        # if feed.lower() == 'yes':
        #     dispatcher.utter_message(text = "આભાર")
        return []

class ActionCountrySearch(Action):

    def name(self) -> Text:
        return "action_country_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "language.csv")
        wals_data = pd.read_csv(data_path)
        data_path_1 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "countrylanguage.csv")
        wals_data_1 = pd.read_csv(data_path_1)
        data_path_2 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "country.csv")
        wals_data_2 = pd.read_csv(data_path_2)
        entities = list(tracker.get_latest_entity_values("language"))
        print(entities)

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]['pk']
                out_row = wals_data_1[wals_data_1['language_pk'] == out_row].to_dict('records')[0]['country_pk']
                out_row = wals_data_2[wals_data_2['pk'] == out_row].to_dict('records')[0]['name']
                out_text = "%s ભાષા %s માં બોલાય છે." % (query_lang, out_row)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "માફ કરશો! અમારી પાસે %s ભાષા માટે વિગતો નથી." % query_lang)

        return []

class ActionMacroAreaSearch(Action):

    def name(self) -> Text:
        return "action_macroarea_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "language.csv")
        wals_data = pd.read_csv(data_path)
        data_path_1 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "walslanguage.csv")
        wals_data_1 = pd.read_csv(data_path_1)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]['pk']
                out_row = wals_data_1[wals_data_1['pk'] == out_row].to_dict('records')[0]['macroarea']
                out_text = "%s ભાષા %s માં બોલાય છે." % (query_lang, out_row)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "માફ કરશો! અમારી પાસે %s ભાષા માટે વિગતો નથી." % query_lang)

        return []       