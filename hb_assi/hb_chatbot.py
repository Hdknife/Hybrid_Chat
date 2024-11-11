"""importing the  nessasary libraries and modules which help
to create the model ...\__-_/
"""
import os
import json
import random
# import emoji
from joblib import dump, load
from scipy.sparse import hstack
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from hv_chatbot.config import (SETTING, logging, feature_1, feature_2, feature_3)
import requests


class HB_Assi:


    """constructor contain name, dataset, retrain_threshodl"""
    def __init__(self, name : str, dataset : dict, retrain_threshold : int | None = 2):
        self.name = name
        self.dataset = dataset
        self.retrain = SETTING.get("retrain")
        self.short_memory : list  = []
        self.history = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.ns_vectorizer = TfidfVectorizer(stop_words=None)
        self.classifier = MultinomialNB()

        if os.path.exists(f"{self.name}.joblib"):
           try:
               self.load_model()
               print("Model loaded successfully!")
               logging.info("Model loaded successfully")
           except Exception as e:
                logging.error(f"Error loading model: {e}")
                return "Some issue in loading the model"
        else:
            try:
                self.train_model()
                logging.info("Model trained successfully")
                self.save_model()
                logging.info("Model saved successfully")
            except Exception as e:
                logging.error(f"Error training and saving model: {e}")
                return "Some issue in training the model"

    def __joinder(self, text_):
        text_ = text_.split()
        if self.name.lower() in text_:
            return text_[0]+' '+ '_'.join(text_[1:])
        return ' '.join(text_)

    def __fit(self):
        return (
        self.vectorizer.fit_transform([question["question"].format(self.name).lower()
        for question in self.dataset]),
        self.ns_vectorizer.fit_transform([question["question"].lower()
        for question in self.dataset])
        )

    def save_model(self):
        try:
            dump(self.classifier, f"{self.name}.joblib")
            logging.info("Model saved successfully")
        except Exception as e:
            logging.error(f"Error saving model: {e}")

    def load_model(self):
        try:
            self.load_dataset_json()
            self.classifier = load(f"{self.name}.joblib")
            self.__fit()
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return "Some issue in loading the model"

    def train_model(self):
        try:
            X_with_stopwords, X_no_stopwords = self.__fit()
            labels = [id["id"] for id in self.dataset]
            transformed_texts = hstack([X_with_stopwords, X_no_stopwords])
            logging.info("texts successfull fited")
            self.classifier.fit(transformed_texts, labels)  # Fit classifier directly
            logging.info("Model trained successfully")
            # print("training succussfull")
        except Exception as e:
            logging.error(f"Error training model: {e}")

    def increment_retrain_count(self):
        try:
            self.train_model()
            self.save_model()
            self.load_model()
            self.save_dataset_json()
            self.short_memory.clear()
            logging.info ("Successful model fine-tune")
        except Exception as e:
            logging.error(f"Error incrementing retrain count: {e}")

    def features_selector(self, question : str, id):
        try:
            if id == 7:
                enable = feature_1.get("active", False)
                if enable:
                    generate = feature_1.get("fun")(question)
                    response = json.loads(generate.replace("```json", "").replace("```", ""))
                    self.short_memory.append({"id": len(self.dataset) + 1,
                                            "question": response.get("question"),
                                            "answers": [response.get("answer")]})
                    return response.get("answer")

            elif id == 8:
                    enable = feature_2.get("active")
                    if enable:
                        response = feature_2.get("fun")
                        title, summary = response.get_summary_of_first_result(input("please enter the topic : "), sentences=3)
                        self.short_memory.append({"id": len(self.dataset) + 1,
                                                "question": title,
                                                "answers": [summary]})
                        return summary

            elif id == 14:
                enable = feature_3.get("active")
                if enable:
                    status, temperature = feature_3.get("fun")
                    API_key = requests.api
                    weather_emoji = ""
                    if "rain" in status.lower():
                        weather_emoji = ":umbrella_with_rain_drops:"
                    elif "clear" in status.lower():
                        weather_emoji = ":sunny:"
                    elif "cloud" in status.lower():
                        weather_emoji = ":cloud:"
                    elif "snow" in status.lower():
                        weather_emoji = ":snowflake:"
                    elif "haze" in status.lower():
                        weather_emoji = ":fog:"
                    return f"Today’s weather is {status} {weather_emoji} with a temperature of {round(temperature,1)}°C."
            elif id == 1:
                return random.choice(self.responses[id - 1]).format(self.name)
            return random.choice(self.responses[id - 1]).format(self.name)

        except Exception as e:
            logging.error(f"Error in features_selector id {id}: {e}")
            return e

    def decoder(self):
        try:
           return [answers['answers'] for answers in self.dataset]
           logging.info("Successful decoder")
        except Exception as e:
            logging.error(f"Error in decoder: {e}")
            return e

    def prediction(self, question : str, m : bool = None):
        try:
            if m:
                question = self.__joinder(question)
            self.responses = self.decoder()
            transformed_sample_with_stopwords = self.vectorizer.transform([question])
            transformed_sample_no_stopwords = self.ns_vectorizer.transform([question])
            transformed_sample_combined = hstack([transformed_sample_with_stopwords, transformed_sample_no_stopwords])
            predicted_id = self.classifier.predict(transformed_sample_combined)
            print(predicted_id)
            logging.info(f"Predicted successfully ID: {predicted_id}")
            return self.features_selector(question, predicted_id[0])
        except Exception as e:
            logging.error(f"Error in prediction: {e}")
            return "Sorry, I couldn't process that."

    def run(self):

        while True:
            query = input("User : ").lower()
            if query.lower() == "exit":
                print("{} : Goodbye!")
                break
            predict = self.prediction(self.__joinder(query))
            # print("Bot_understand:", self.__joinder(query))
            print("Bot:", predict)
            if SETTING.get("enable_history_save", False):
                feedback = input("please give me the feedback enter yes(Y),Not(N) :").lower()
                self.history.append({"user-question": query,
                                     "id" : self.short_memory[0].get("id") if self.short_memory else '',
                                     "question":self.short_memory[0].get("question") if self.short_memory else query,
                                     "answer": predict,
                                     "feedback" : True if "y"  else False})
                if SETTING.get("retrain"):
                    if self.short_memory:
                       for i in self.history:
                          if i.get("feedback") and i.get("id") == self.short_memory[0].get('id'):
                             self.dataset.extend(self.short_memory)
                            #  print("Dataset is extending")
                             self.increment_retrain_count()
                else:
                    self.short_memory.clear()


    def save_dataset_json(self):
        with open(f"{self.name}.json", "w") as file:
            json.dump(self.dataset, file, indent = 2)
            # print("Dataset saved successfully!")
            logging.info("Dataset saved successfully")

    def load_dataset_json(self):
        try :
           with open(f"{self.name}.json", "r") as file:
               self.dataset = json.load(file)
            #    print("Dataset loaded successfully!")
               logging.info("Dataset loaded successfully")

        except:
            return self.dataset
            # loginig.err"Some issue in loading the dataset"
    def summary(self):
        return f"""
        Chatbot name : {self.name}
        Traning parameter : {len(self.dataset)}
        ...\___-_/
        """
