from enum import Enum
from constants.interface import *

class UploadStatus(Enum):
    
    EMPTY = 0
    ERROR = 1
    EXISITING = 2

class InputStatus(Enum):

    EMPTY = 0
    ERROR = 1
    EXISTING = 2

class SelectionStatus(Enum):

    DEFAULT = 0
    CHANGED = 1



NOTEBOOK_UPLOAD_STATUS = {

    WidgetText.WARNING.value:'存在当前未翻译的 Notebook',
    WidgetText.ERROR.value:'无法解析上传的 Notebook',

}
