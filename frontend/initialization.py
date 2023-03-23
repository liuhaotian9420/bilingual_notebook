from frontend.constants.constants import *

def InitializeState(session_state,):

    
    if session_state.get('activate_download_button') is None:
        
        session_state['activate_download_button'] = False

    if session_state.get('cached_results') is None:

        session_state['cached_results'] = None

    if session_state.get('notebook_upload_status') is None:
        
        session_state['notebook_upload_status'] = UploadStatus.EMPTY.value

    if session_state.get('api_key_input_status') is None:
        
        session_state['api_key_input_status'] = InputStatus.EMPTY.value

    if session_state.get('runs') is None:

        session_state['runs'] = False

    if session_state.get('source_language_select_status') is None:
        
        session_state['source_language_select_status'] = SelectionStatus.DEFAULT.value


    if session_state.get('target_language_select_status') is None:
        
        session_state['target_language_select_status'] = SelectionStatus.DEFAULT.value


    if session_state.get('model_selection_status') is None:
        
        session_state['model_selection_status'] = SelectionStatus.DEFAULT.value