import os
import sys
import json
import numpy as np
import pandas as pd
import functools
import re
from utils.notebook_parser import parse_comment
from collections import Counter, defaultdict


def is_path(string):

    return os.path.isdir(string) or os.path.isfile(string)


class Notebook():

    def __init__(self, meta:dict=None,content:defaultdict(list)=None):

        '''
        meta: dictionary containing meta information about the notebook,including kernelspec,languageinfo and file_extensions
        content: dictionary containing information, also containing origini cell order
        
        '''
        # print('FLAG INIT: input content is:',len(content['markdown']))
        self.meta = meta
        self.content = defaultdict(list)
        self.cells = None
        self.line_counter = 0
        # print('FLAG INIT:self.content is:',len(self.content['markdown']))


    def loads(self, ipynb:str):

        '''
        ipynb: can be either a string or a valid ipynb filepath
        
        '''
 
        if self.cells is not None:

            return self

        
        if is_path(ipynb):

            nb_json = json.load(open(ipynb,'r'))

        else:
            
            nb_json = json.loads(ipynb)

        # check if ipynb file contains cells
        assert 'cells' in nb_json.keys(), 'No cells found in notebook'


        content  = self._get_content()

        for idx,cell in enumerate(nb_json['cells']):

            if cell['cell_type'] == 'markdown':
                
                self.line_counter +=  len(cell['source'])

            content[cell['cell_type']].append((idx,cell))
            
        self.cells = nb_json['cells']

        # update meta of notebook
        self.meta = nb_json['metadata'] 
    

    def get_markdown(self):

        return self.content['markdown']
    
    def _get_content(self):

        # print('self.content is:',len(self.content['markdown']))

        return self.content

    def get_code(self):

        return self.content['code']
        
    def set_cell(self, cell):
        '''
        cell: a tuple containing (cell_index,cell_value)
        '''
        cell_index = cell[0]
        cell_value = cell[1]
        self.cells[cell_index]['source'] = cell_value

    def reconstruct(self):

        '''
        rebuild the notebook from its contents
        '''

        nb = {}
        nb['metadata'] = self.meta
        nb['cells'] = self.cells
        nb['nbformat'] = 4
        nb['nbformat_minor']=0

        return nb