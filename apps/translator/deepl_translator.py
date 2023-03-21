import json
import time
import requests
import deepl

from utils.language_dict import LANGUAGES,TO_LANGUAGE_CODE,standardize_language_string
from .base_translator import baseTranslator

class DeepL(baseTranslator):
    """
    deepl-translator, mainly consists of deeplXpython package
    """

    def __init__(self, key, source_language, target_language, **kwargs):
        super().__init__(key, source_language, target_language)

        # self.api_url = "https://deepl-translator.p.rapidapi.com/translate"
        
        # self.headers = {
        #     "content-type": "application/json",
        #     "X-RapidAPI-Key": "",
        #     "X-RapidAPI-Host": "deepl-translator.p.rapidapi.com",
        # }
        # print('FLAG REVERSE SET:',standardize_language_string(source_language.lower(),reverse=True))
        self.source_language = standardize_language_string(source_language.lower(),reverse=True)
        self.target_language = standardize_language_string(target_language.lower(),reverse=True)
        self.active_key = ''

        # if self.source_language == 'en':
        #     self.source_language = 'en-US'

        # if self.target_language == 'en':
        #     self.target_language = 'en-US'

        # if self.source_language not in [
        #     "bg",
        #     "zh",
        #     "cs",
        #     "da",
        #     "nl",
        #     "en-US",
        #     "en-GB",
        #     "et",
        #     "fi",
        #     "fr",
        #     "de",
        #     "el",
        #     "hu",
        #     "id",
        #     "it",
        #     "ja",
        #     "lv",
        #     "lt",
        #     "pl",
        #     "pt-PT",
        #     "pt-BR",
        #     "ro",
        #     "ru",
        #     "sk",
        #     "sl",
        #     "es",
        #     "sv",
        #     "tr",
        #     "uk",
        #     "ko",
        #     "nb",
        # ]:
        #     raise Exception(f"DeepL do not support {self.source_language}")


    def rotate_key(self):

        self.active_key = f"{next(self.keys)}"

    def translate(self, text):
        self.rotate_key()
        # payload = {"text": text, "source": self.source_language, "target": self.target_language}
        
        translator = deepl.Translator(self.active_key)


        try:
            response = translator.translate_text(text,source_lang=self.source_language,target_lang=self.target_language,tag_handling='xml', ignore_tags=['x'])
        except Exception as e:
            # print(str(e))
            time.sleep(20)
            response = translator.translate_text(text,source_lang=self.source_language,target_lang=self.target_language,tag_handling='xml', ignore_tags=['x'])

        t_text = response.text
        # print(response.text)
        return t_text