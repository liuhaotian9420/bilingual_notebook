import itertools
import re


tc = itertools.cycle(['<x>','</x>'])

compilers = {

    'url': re.compile(r'\(http.+?\)', re.DOTALL),
    'image': re.compile(r'!\[.+?\]', re.DOTALL),
    'package_alias': re.compile(r'(?<=import\s)[\w+\s*,*]+(?=\sas\s)|(?<=\sas\s)[\w+,*]+'),
    'tq': re.compile(r'(?<=""")[^"""]+(?=""")'),
    'dq': re.compile(r'(?<=\'\'\')[ ^\'\'\']+(?=\'\'\')'),
    'ns': re.compile(r'(?<=#)[^\n\r]+(?=\n)|(?<=#)[^\n\r]+(?=\r)'),
    'package': re.compile(r'(?<=import\s)[\w+\s*,*]+|(?<=\sas\s)[\w+,*]+'),
    'path': re.compile(r'(?<=\').*/\w*\d*'),
    'entity': re.compile(re.compile(r'.*?=')),
    'func': re.compile(r'\.*\w+\d*\(.*\)'),
    'splitter': re.compile(r'\w+|='),
    'value': re.compile(r'=.*'),
    'tabspace': re.compile(r'^[\s|\t]+\w*?'),
    'header':re.compile(r'(^#{1,6})\s(.*)'),
    'bullets':re.compile(r'(\d+\.|-) (.*)'),
    'code':re.compile(r'`'),
    }

skippers = ['\n','$$','$','$\n','$$\n']


def pop_code(match):

    return next(tc)

def parse_comment(text:list, comment_type:str ='ns'):

    '''
    text:
    - text to be parsed
    - can be instances of iterables of str or one complete string

    comment_type:
    - comment_types to be parsed out, a string
    - available type: 'ns'(#),'dq'(double quote),'tq'(triple quote)
    - default: 'ns'

    returns the parsed out comments and the filtered text

    '''
    text = ''.join(text)
    comment_compiler = compilers[comment_type]
    comments = re.findall(comment_compiler, text)
    return ''.join(comments), re.sub(comment_compiler, '', text)

def parse_package(text):
    '''
    text:
    - text to be parsed
    - can be instances of iterables of str or one complete string

    returns the alias:package dict

    '''

    imports = []
    alias_package = {}

    if ' as ' in text:

        imports = re.findall(compilers['package_alias'], text)

    else:

        imports = re.findall(compilers['package'], text)

    if not len(imports):

        return {}

    package_names = re.sub(' ', '', imports[0]).split(',')

    if len(imports) > 1:

        aliases = re.sub(' ', '', imports[1]).split(',')
    else:
        aliases = []

    for i in range(len(package_names)):

        if i > len(aliases)-1:

            alias_package.update({package_names[i]: package_names[i]})

        else:

            alias_package.update({aliases[i]: package_names[i]})

    return alias_package


