import streamlit as st
import time
from scripts.constants.constants import *
from constants.interface import WidgetText as wt
from apps.main import get_model,markdown_line_translate
from apps.notebook import Notebook
from random import random



def TranslationProgressing(model,notebook,progress_bar):

    counter = 0

    for idx, md in notebook.get_markdown():

        translated_pct = int((counter+random()*len(md['source']))/notebook.line_counter*100)

        progress_bar.progress(
                              translated_pct, 
                              text= TRANSLATE_PROGRESS_BAR[wt.LOG.value].format(lines_translated=str(translated_pct)))
        
        notebook.set_cell((idx, markdown_line_translate(md['source'],model,)))

        counter+= len(md['source'])
        
        translated_pct= int(counter/notebook.line_counter*100)

        progress_bar.progress(
                              translated_pct, 
                              text= TRANSLATE_PROGRESS_BAR[wt.LOG.value].format(lines_translated=str(translated_pct)))
    
    
    return notebook


def UploadNotebook(session_state,wid:str):

    '''
    session_state: 当前应用的 session_state
    wid: string, 当前 widget 的id
    '''
    current_status = session_state.get('notebook_upload_status') 

    if not session_state[wid] and current_status is not None:

        session_state['notebook_upload_status'] = UploadStatus.EMPTY.value

        return


    if (current_status is not None) and (current_status == UploadStatus.EXISITING.value) and session_state[wid]:
        
        st.error(NOTEBOOK_UPLOAD_STATUS[wt.WARNING.value]+': '+session_state[wid].name)
        
        return 

    notebook_file = session_state[wid]

    try:
        nb_json = notebook_file.getvalue().decode("utf-8")
        nb = Notebook()
        nb.loads(nb_json)
        session_state['notebook_upload_status'] = UploadStatus.EXISITING.value
        session_state['notebook'] = nb
        session_state['cached_results'] = None

    except:
    
       session_state['notebook_upload_status'] = UploadStatus.ERROR
       st.error(NOTEBOOK_UPLOAD_STATUS[wt.ERROR.value]+': '+session_state[wid].name)

def ModelSelection(session_state, wid):

    if session_state[wid]:

        session_state['model'] = session_state[wid].strip()

    else:

        session_state['model'] = 'deepl'


def APIKeyInput(session_state, wid):

    # assert session_state['api_key_input_status'] != APIKeyInputStatus.EXISTING.value
    # assert session_state.get('model') is not None 
    session_state['api_key_input_status'] = InputStatus.EXISTING.value
    session_state['key'] = session_state[wid].strip()    
    
    # return session_state
        
def LanguageSelection(session_state, wid, is_source=True):

    if is_source:

        session_state['source_language'] = session_state[wid].strip()
        session_state['source_language_select_status'] == SelectionStatus.CHANGED.value

    else:

        session_state['target_language'] = session_state[wid].strip()
        session_state['target_language_select_status'] == SelectionStatus.CHANGED.value


def ClickTranslate(session_state,logger,progress):

    if session_state['notebook_upload_status'] != UploadStatus.EXISITING.value:

        logger.error(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.ERROR.value]['ipynb_not_found'],icon = '🔥')

        return

    if session_state['api_key_input_status'] != InputStatus.EXISTING.value:

        logger.error(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.ERROR.value]['key_not_found'],icon = '🔑')

        return


    key = session_state['key']
    
    # use default values in selection box if not explicitly set

    if session_state['model_selection_status'] != SelectionStatus.DEFAULT.value:
    
        model_name = session_state['model']
    
    else:
        model_name = 'deepl'

    if session_state['source_language_select_status'] != SelectionStatus.DEFAULT.value:

        source_language = session_state['source_language']
    
    else:
        source_language = 'english'

    if session_state['target_language_select_status'] != SelectionStatus.DEFAULT.value:
        
        target_language = session_state['target_language']

    else:
        target_language = 'simplified chinese'

    model = get_model(model_name,key,source_language,target_language)

    line_counts = session_state['notebook'].line_counter

    ### loggin
    logger.empty()
    logger.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.LABEL.value].format(source_language=source_language, 
                                                                              target_language=target_language))
    logger.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.HELP.value].format(model_name=model_name))
    logger.write(DISPLAYED_TEXT_WHEN_COMPUTING_MD_META[wt.LABEL.value])
    time.sleep(2)
    logger.write(DISPLAYED_TEXT_WHEN_COMPUTING_MD_META[wt.SUCCESS.value].format(line_counts=line_counts))
    logger.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.SUCCESS.value])


    progress_bar  = progress.progress(0,text=TRANSLATE_PROGRESS_BAR[wt.LABEL.value])    

    notebook = TranslationProgressing(model,session_state['notebook'],progress_bar).reconstruct()
    
    session_state.activate_download_button = True
    session_state.runs = True
    session_state.cached_results = notebook
    


    





    