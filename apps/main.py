import re

from .notebook import Notebook 
from .translator.gpt3_translator import GPT3
from .translator.deepl_translator import DeepL
from utils.notebook_parser import skippers,compilers,pop_code
from tqdm import tqdm


def get_model(name, key, source_language, target_language,**kwargs):

    if name == 'gpt-3.5':

        return GPT3(key, source_language, target_language,**kwargs)

    if name == 'deepl':

        return DeepL(key, source_language, target_language,**kwargs)
    
def tag_mask(md:str):

    return re.sub(compilers['code'],pop_code,md)

def markdown_line_translate(md:list[str],model,):

    bilingual_mds = []

    # if not session_state.get('line_counter'):
    #     session_state['line_counter'] = 0

    for m in tqdm(md):

        if m.replace(' ','').replace('\t','').replace('-','') in skippers:

            bilingual_mds.append(m)

        elif re.findall(compilers['header'],m):

            header_level, header = re.findall(compilers['header'],m)[0]
            ttext = re.sub('<x>|</x>','`',model.translate(tag_mask(header)))
            bilingual_mds.append(header_level
                                 + ' '
                                 + header
                                 + '\n'
                                 + header_level
                                 + ' '
                                 + ttext 
                                 + '\n')

        elif re.findall(compilers['bullets'],m):

            bullet_index, bullet_point = re.findall(compilers['bullets'],m)[0]
            ttext = re.sub('<x>|</x>','`',model.translate(tag_mask(bullet_point)))
            bilingual_mds.append(bullet_index
                                 + ' '
                                 + bullet_point
                                 + '\n'
                                 + ' '*len(bullet_index)*2
                                 + ttext 
                                 + '\n\n')
        else:

            ttext = re.sub('<x>|</x>','`',model.translate(tag_mask(m)))

            if ttext != m:
                bilingual_mds.append(m+'\n'+ttext+'\n')
            else:
                bilingual_mds.append(m+'\n')
                
    return bilingual_mds
        

