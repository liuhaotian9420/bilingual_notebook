from enum import Enum

class WidgetText(Enum):
    '''
    ID:      组件的ID,用来区分同一 container 下同一类型的不同组件
    LABEL:   组件的展示标签
    HELP:    组件的帮助提示，在组件右上角的 ？ 中可以看到
    WARNING: 组件告警
    SUCCESS: 组件运行成功提示
    ERROR:   组件报错提示
    '''
    ID = 0
    LABEL = 1
    HELP = 2
    WARNING = 3
    SUCCESS = 4
    ERROR = 5
    OUTPUT = 6
    LOG = 7

############################ 参数输入 ####################################

NOTEBOOK_UPLOADER = {
    WidgetText.ID.value:'nb_uploader',
    WidgetText.LABEL.value:'上传你的 Jupyter Notebook文件',
    WidgetText.HELP.value:'请确保上传的 ipynb 文件为合法文件',
}

MODEL_SELECTION_BOX = {
    WidgetText.ID.value:"translator_model_selection_box",
    WidgetText.LABEL.value:"选择使用的模型",
    WidgetText.HELP.value:"对于含有较多代码块的文本，推荐使用DeepL"
}

API_KEY_INPUT_BOX = {
    WidgetText.ID.value:"api_key_input_box",
    WidgetText.LABEL.value: "输入你的 {translator_model} key"
}

SOURCE_LANGUAE_SELECTION_BOX = {
    WidgetText.ID.value:'source_language_selection_box',
    WidgetText.LABEL.value:"源语言",
}

TARGET_LANGUAE_SELECTION_BOX = {
    WidgetText.ID.value:'target_language_selection_box',
    WidgetText.LABEL.value:"目标语言",
}

############################ 核心功能 ####################################



TRANSLATE_BUTTON = {
    WidgetText.ID.value:"translate_button",
    WidgetText.LABEL.value:"翻译",
    WidgetText.ERROR.value:"报错:{error_message}",
    WidgetText.SUCCESS.value:"翻译完成",
}

# 置灰的下载按钮
DUMMY_DOWNLOAD_BUTTON = {
    WidgetText.ID.value:"download_button_dummy",
    WidgetText.LABEL.value:"下载",
    WidgetText.HELP.value:"翻译完成后下载"
}

ACTIVE_DOWNLOAD_BUTTON = {
    WidgetText.ID.value:"download_button_active",
    WidgetText.LABEL.value:"下载",
    WidgetText.SUCCESS.value:"下载成功！"
}

############################ 页面展示 ####################################

PAGE_TITLE = {
    WidgetText.LABEL.value:"Bilingual Jupyter Notebook :ringed_planet:",
}

PAGE_MAJOR_INFO = {
    WidgetText.LABEL.value:'''
    QUality of translation might not be perfect and proofreading is recommended

    Translation speed is determined by:

    1. Lines of markdown cell

    2. Words in each line

    Powerd by OpenAI GPT-3.5 Turbo

''',
}

DISPLAYED_TEXT_WHEN_INIT_TRANSLATING = {
    WidgetText.LABEL.value:"正在将 Jupyter Notebook 从 {source_language} 转为 {target_language}。",
    WidgetText.SUCCESS.value:"开始翻译", 
    WidgetText.HELP.value:"使用 {model_name} 模型", 
    WidgetText.ERROR.value:{"ipynb_not_found":"未找到 ipynb 文件",
                            "key_not_found":"未找到 API key"}

}

DISPLAYED_TEXT_WHEN_COMPUTING_MD_META = {
    WidgetText.LABEL.value:"计算当前文件的 Markdown 大小",
    WidgetText.SUCCESS.value:"当前文件共有 {markdown_counts} 个 Markdown cell, 总计 {line_counts} 行文本", 
}



############################ 其他 ####################################


MORE_OPTIONS_SHOW_BUTTON = {
    WidgetText.ID.value:"show_more_button",
    WidgetText.LABEL.value:"更多选项",
}

TRANSLATE_PROGRESS_BAR = {
    WidgetText.ID.value:"translate_progress_bar",
    WidgetText.LABEL.value:"正在翻译中,请稍候",
    WidgetText.WARNING.value: "cell 数量较多",
    WidgetText.LOG.value: "已翻译 {lines_translated} %的行数",
}



