
import time
import streamlit

from constants.interface import *
from constants.interface import WidgetText as wt


def start_translation(container,**kwargs):

    source_language = kwargs.get('source_language',None)
    target_language = kwargs.get('target_language',None)
    model = kwargs.get('model',None)
    container.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.LABEL.value].format(source_language=source_language, 
                                                                              target_language=target_language))
    container.write(DISPLAYED_TEXT_WHEN_INIT_TRANSLATING[wt.HELP.value].format(model_name=model))
    container.write(DISPLAYED_TEXT_WHEN_COMPUTING_MD_META[wt.LABEL.value])
    time.sleep(2)
