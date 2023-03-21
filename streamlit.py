import streamlit as st
import time
import json
import os

# from streamlit import SessionState
from apps.notebook import Notebook
from io import StringIO
from apps.main import markdown_line_translate,get_model
from utils.notebook_parser import skippers

# Title and info panel for bilignual jupternotebook

from utils.language_dict import LANGUAGES, TO_LANGUAGE_CODE


ALL_LANGUAGES = [k.capitalize() for k in list(TO_LANGUAGE_CODE.keys())]

if 'is_processing' not in st.session_state:

    st.session_state['is_processing'] = False

st.cache_data.clear()

st.title("Bilingual Jupyter Notebook :ringed_planet:")
st.info('''
    QUality of translation might not be perfect and proofreading is recommended

    Translation speed is determined by:

    1. Lines of markdown cell

    2. Words in each line

    Powerd by OpenAI GPT-3.5 Turbo

''')


nb_loader = st.container()
nb_loader.empty()

file = nb_loader.file_uploader("上传你的 Jupyter Notebook 文件", type=".ipynb",help="请确保上传的是合法的 ipynb 文件")

nb = None

if file:
    nb_json = file.getvalue().decode("utf-8")
    nb = Notebook()
    nb.loads(nb_json)
    st.session_state['is_processing'] = True
    # st.write('After:',id(nb),str(len(nb.get_markdown())))
    md_counts= len(nb.get_markdown())
    


# 翻译相关

translator_model, key_input = st.columns(2)

model = translator_model.selectbox("选择使用的模型",options=['gpt-3.5','deepl'])
# translator_model.session_state['model'] = 'gpt-3.5'

if model is not None:
    
    key = key_input.text_input("输入你的 Key",type='password')

if st.checkbox('Additional Options'):

    src_language,trgt_language = st.columns(2)
    source_language=src_language.selectbox("Source Language",ALL_LANGUAGES).lower()
    target_language=trgt_language.selectbox("Target Language",ALL_LANGUAGES).lower()

else:

    source_language= 'english'
    target_language= 'simplified chinese'

info_container = st.container()
pbar_container = st.container()
start, downloads = st.columns(2)
dl = downloads.empty()

download = dl.download_button(label="Download",
                              data='some text to be downloaded',
                              file_name='a sample_name', 
                              mime="application/ipynb",
                              disabled=True,
                              key = 'the dummy download button')

w1,w2 = start.columns([2,1])






def start_translation(nb,model,source_language, target_language):

    info_container.write('正在将 Jupyter Notebook 从 '+source_language+' 转为 '+target_language+' 。')
    info_container.write('使用'+model+'模型')
    info_container.write('计算当前 Markdown 大小...')
    time.sleep(2)
    info_container.write('当前 Notebook 共有 '+ str(len(nb.get_markdown()))+' 个 markdown cell，总计 '+str(nb.line_counter)+' 行')
    info_container.write('开始翻译')


translate_button = w2.button("Translate", on_click=start_translation, args=(nb, model, source_language, target_language ))

translator_model = get_model(model,key,source_language,target_language)


if translate_button:

    progress_bar  = pbar_container.progress(0,text='正在翻译中,请稍后')
    
    counter = 0 

    for idx, md in nb.get_markdown():

        st.write(len(md['source']))
        nb.set_cell((idx, markdown_line_translate(md['source'],translator_model)))
        counter+= len(md['source'])
        progress_bar.progress(int(counter/nb.line_counter*100), text='正在翻译中，已翻译'+str(int(counter/nb.line_counter*100))+'% 的行数')

    dl.empty()
    
    translated_notebook = nb.reconstruct()

    st.session_state['is_processing'] = False

    download1 = dl.download_button(key = 'the real one',label="Download", data=json.dumps(translated_notebook), file_name='a sample_name.ipynb', mime="application/ipynb",disabled=False)
