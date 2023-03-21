# import json

# from apps import notebook
# from apps.main import translate_notebook
# from utils.notebook_parser import skippers

# # nb = notebook.Notebook()
# # nb.loads('1-1_Anaconda_Installation.ipynb')

# # print(skippers)

# # print(nb.get_markdown()[0][1]['source'][2] in skippers)


# new_nb = translate_notebook('1-1_Anaconda_Installation.ipynb','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,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','gpt3','english','simplified chinese')

# with open('test_new.ipynb','w') as test:
#     json.dump(new_nb,test)


# print(None is not None)


# import requests

# url = "https://deepl-translator.p.rapidapi.com/translate"

# payload = {
# 	"text": "This is a example text for translation.",
# 	"source": "EN",
# 	"target": "ZH"
# }
# headers = {
# 	"content-type": "application/json",
# 	"X-RapidAPI-Key": "c02103ae14mshfaecb4b51181618p18c7aejsna58e8015cf7c",
# 	"X-RapidAPI-Host": "deepl-translator.p.rapidapi.com"
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)



import deepl

auth_key = "d7b157ba-3c3c-8eb8-9d40-633b332b064e:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

result = translator.translate_text("Hello, world!", target_lang="FR")
print(result.text)  # "Bonjour, le monde !"