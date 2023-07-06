import json
import time
import requests
import deepl

from constants.languages import LANGUAGES,TO_LANGUAGE_CODE,standardize_language_string
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
        self.source_language = standardize_language_string(source_language.lower(),reverse=True).upper()
        self.target_language = standardize_language_string(target_language.lower(),reverse=True).upper()
        self.active_key = ''

        if self.target_language == 'EN':
            self.target_language = 'EN-US'

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
            print('FLAG SELF SOURCE LANG:',self.source_language)

            response = translator.translate_text(text,source_lang=self.source_language,target_lang=self.target_language,tag_handling='xml', ignore_tags=['x'])

        t_text = response.text
        return t_text

    def get_glossary_languages(self):

        self.rotate_key()

        translator = deepl.Translator(self.active_key)

        return translator.get_glossary_languages()