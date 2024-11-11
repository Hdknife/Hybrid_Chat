# config.py
import os
import logging
import datetime
import dotenv
# from hv_chatbot.wiki import Wikipedia
from hv_chatbot.weather import weather_status
from hv_chatbot.gimini import Gemini


dotenv.load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

Prompt :str.upper =  """
Query : You Task is To give the Proper Summarize Answer Of Question!.
Question_Catagiery Should Only Answer Related : ["Space", "AI","Bunessiness"]
User_Question : {}?
Answer : Answer Should only will be answer and no other text!
Formate = json random id question : conver into proper question remove gimini or any used gimin etc and answer : ""
"""

Prompt_Email : str.upper = """
Query : Your task is Write an Emails Response.
User_Question : {QUESTION}?
Answer : Answer Should only will be answer and no other text!
"""

SETTING = {
    "AI_Module" : True,
    "Wiki_Module" : True,
    "Model_API" : os.getenv('AI_API', False),
    "Model" : os.getenv("MODEL"),
    "Prompt" : {'topic': Prompt,'email' : Prompt_Email},
    "maximum_token_generation" : 70,
    "Wether_Module" : True,
    "date" : datetime.datetime.now().strftime("%d-%m-%Y"),
    "time_zone" : "Asia/Kolkata",
    "retrain" : True,
    "Weather_API": os.getenv('WEATHER_API'),
    "enable_history_save" : True,
    "history_save_mongo" : False,
    "history_save_sql" : False,
    "model_save_folder" : "/",
    "database_ip_address" : "",
}

feature_1 = {
 "id" : 7,
 "name" :"gimini",
 "active" : SETTING.get("AI_Module",False),
 "fun" : Gemini(SETTING,Prompt= Prompt).generate_response
 }

feature_2 = {
 "id" : 8,
 "name" :"wiki",
 "active" : SETTING.get("Wiki_Module",False),
#  "fun" : Wikipedia(language="en")
 }

feature_3 = {
 "id" : 14,
 "name" :"wether",
 "active" : SETTING.get("Wether_Module",False),
 "fun" :  weather_status("jabalpur", SETTING['Weather_API'])
 }
