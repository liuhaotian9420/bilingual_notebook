import requests
from rich import print

from .base_translator import baseTranslator


class GPT3(baseTranslator):
    def __init__(self, key, src_language, target_language, api_base=None, prompt_template=None, **kwargs):

        super().__init__(key, src_language, target_language)

        self.api_url = (
            f"{api_base}v1/completions"
            if api_base
            else "https://api.openai.com/v1/completions"
        )
        self.headers = {
            "Content-Type": "application/json",
        }

        # TODO support more models here
        self.data = {
            "prompt": "",
            "model": "text-davinci-003",
            "max_tokens": 1024,
            "temperature": 1,
            "top_p": 1,
        }

        self.session = requests.session()


        self.prompt_template = (

            prompt_template or "Please help me to translate, `{text}`  from {source_language} to {target_language}. Ignore text wrapped by <x> and </x>"

        )

    def rotate_key(self):

        self.headers["Authorization"] = f"Bearer {next(self.keys)}"


    def translate(self, text):

        self.rotate_key()
        self.data["prompt"] = self.prompt_template.format(

            text=text, source_language=self.source_language, target_language=self.target_language
        )

        r = self.session.post(self.api_url, headers=self.headers, json=self.data)
        
        if not r.ok:
            print(r.text)
            return text

        t_text = r.json().get("choices")[0].get("text", "").strip()

        return t_text