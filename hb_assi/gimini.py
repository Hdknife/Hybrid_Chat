
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os




class Gemini:

    def __init__(self, setting, Prompt):
        self.setting = setting
        self.prompt = Prompt

    def create_connection(self):
        try:
            genai.configure(api_key = self.setting.get("Model_API"))
            return genai.GenerativeModel(model_name= self.setting.get("Model"))
        except Exception as e:
            print(e)
            return None

    def generate_response(self, QUESTION : str, prompt_type = 't' ):
        model = self.create_connection()
        if prompt_type == 't':
            text = self.setting["Prompt"].get('topic').format(QUESTION)
        if prompt_type == 'e':
            text = self.setting["Prompt"].get('email').format(QUESTION = QUESTION)
        response = model.generate_content(text,  safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            })

        return response.text