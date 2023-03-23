import streamlit as st
import json

from scripts.callbacks import *
from constants.languages import TO_LANGUAGE_CODE
from constants.interface import *
from constants.interface import WidgetText as wt
from scripts.initialization import InitializeState


InitializeState(st.session_state)

# Widgets are placed in a container
# So all major blocks should be of container type

ALL_LANGUAGES = [k.title() for k in list(TO_LANGUAGE_CODE.keys())]

############################ UI ####################################

introduction = st.container()
introduction.title(PAGE_TITLE[wt.LABEL.value])
introduction.info(PAGE_MAJOR_INFO[wt.LABEL.value])


# 上传 Notebook
nb_uploader = st.container()
file = nb_uploader.file_uploader(NOTEBOOK_UPLOADER[wt.LABEL.value], 
                                 type=".ipynb",
                                 help=NOTEBOOK_UPLOADER[wt.HELP.value],
                                 key=NOTEBOOK_UPLOADER[wt.ID.value],
                                 on_change=UploadNotebook,
                                 args=(st.session_state,NOTEBOOK_UPLOADER[wt.ID.value]),
                                 )


inputs = st.container()
translator_model, key_input = inputs.columns(2)

# 选择翻译模型
model = translator_model.selectbox(
                                    MODEL_SELECTION_BOX[wt.LABEL.value],
                                    options=['deepl','gpt-3.5'],
                                    help=MODEL_SELECTION_BOX[wt.HELP.value],
                                    key=MODEL_SELECTION_BOX[wt.ID.value],
                                    on_change=ModelSelection,
                                    args=(st.session_state,MODEL_SELECTION_BOX[wt.ID.value],),
                                    )
# 输入API-Key
key = key_input.text_input(API_KEY_INPUT_BOX[wt.LABEL.value].format(translator_model=model),
                             key=API_KEY_INPUT_BOX[wt.ID.value],
                             type='password',
                             on_change=APIKeyInput,
                             args=(st.session_state,API_KEY_INPUT_BOX[wt.ID.value],),)

# 更多选项                             
more_options = st.container()
if more_options.checkbox(MORE_OPTIONS_SHOW_BUTTON[wt.LABEL.value]):
    
    src_language,trgt_language = more_options.columns(2)
    source_language=src_language.selectbox(
                                            SOURCE_LANGUAE_SELECTION_BOX[wt.LABEL.value],
                                            options=ALL_LANGUAGES,
                                            key=SOURCE_LANGUAE_SELECTION_BOX[wt.ID.value],
                                            on_change=LanguageSelection,
                                            args=(st.session_state,SOURCE_LANGUAE_SELECTION_BOX[wt.ID.value],),
                                            ).lower()
    target_language=trgt_language.selectbox(
                                            TARGET_LANGUAE_SELECTION_BOX[wt.LABEL.value],
                                            options=ALL_LANGUAGES,
                                            on_change=LanguageSelection,
                                            args=(st.session_state,SOURCE_LANGUAE_SELECTION_BOX[wt.ID.value],),
                                            kwargs={'is_source':False}
                                            ).lower()
    
# Logging
logging = st.container()
logging.empty()
# 进度条
progress = st.container()
progress.empty()


buttons = st.container()
translate, download = buttons.columns(2)
dummy = download.empty()
w1,w2 = translate.columns([2,1])


# 下载按钮
if not st.session_state['activate_download_button']:

    dummy_download = dummy.download_button(DUMMY_DOWNLOAD_BUTTON[wt.LABEL.value],
                                mime="application/ipynb",
                                data = '',
                                disabled=True,
                                key= DUMMY_DOWNLOAD_BUTTON[wt.ID.value],
                                help= DUMMY_DOWNLOAD_BUTTON[wt.HELP.value],)
# 翻译按钮
translate_button = w2.button(
                             TRANSLATE_BUTTON[wt.LABEL.value], 
                             on_click=ClickTranslate, 
                             args=(st.session_state,logging,progress,),
                             )

if translate_button and st.session_state['runs']:
    
    dummy.empty()
    file_name = '[{language_code}]'.format(language_code=TO_LANGUAGE_CODE.get(target_language))+file.name
    active_download = download.download_button(key=ACTIVE_DOWNLOAD_BUTTON[wt.ID.value],
                                               label=ACTIVE_DOWNLOAD_BUTTON[wt.LABEL.value], 
                                               data=json.dumps(st.session_state['cached_results']), 
                                               file_name=file_name,                                                mime="application/ipynb",
                                               disabled=False,)
    nb_uploader.empty()












############################ Scripts ####################################


# nb = None
# if file:
#     nb_json = file.getvalue().decode("utf-8")
#     nb = Notebook()
#     nb.loads(nb_json)
#     md_counts = str(len(nb.get_markdown()))
#     line_counts = str(nb.line_counter)

# translator_model = get_model(model,key,source_language,target_language)


# if not file and translate_button:

#     logging.error(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.ERROR.value]['ipynb_not_found'],icon = '🔥')

# if not key and translate_button:

#     logging.error(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.ERROR.value]['key_not_found'],icon = '🔑')

# if key and file and translate_button:

#     logging.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.LABEL.value].format(source_language=source_language, 
#                                                                               target_language=target_language))
#     logging.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.HELP.value].format(model_name=model))
#     logging.write(DISPLAYED_TEXT_WHEN_COMPUTING_MD_META[wt.LABEL.value])
#     time.sleep(2)
#     logging.write(DISPLAYED_TEXT_WHEN_COMPUTING_MD_META[wt.SUCCESS.value].format(markdown_counts=md_counts,line_counts=line_counts))
#     logging.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.SUCCESS.value])
    
#     progress_bar  = progress.progress(0,text=TRANSLATE_PROGRESS_BAR[wt.LABEL.value])
#     counter = 0 

#     for idx, md in nb.get_markdown():

#         nb.set_cell((idx, markdown_line_translate(md['source'],translator_model)))
#         counter+= len(md['source'])
#         lines_translated = int(counter/nb.line_counter*100)
#         progress_bar.progress(int(counter/nb.line_counter*100), 
#                               text= TRANSLATE_PROGRESS_BAR[wt.LOG.value].format(lines_translated=str(lines_translated)))


#     translated_notebook = nb.reconstruct()
#     dummy.empty()

#     # 更新下载按钮

#     file_name = '[{language_code}]'.format(language_code=TO_LANGUAGE_CODE.get(target_language))+file.name
#     active_download = download.download_button(key=ACTIVE_DOWNLOAD_BUTTON[wt.ID.value],
#                                                label=ACTIVE_DOWNLOAD_BUTTON[wt.LABEL.value], 
#                                                data=json.dumps(translated_notebook), 
#                                                file_name=file_name, 
#                                                mime="application/ipynb",
#                                                disabled=False,)
