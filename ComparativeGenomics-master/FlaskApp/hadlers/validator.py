import polars as pl
from skbio import TreeNode
from io import StringIO
import re

def template(allowed_file_types, data, columns, error):
    content = pl.DataFrame()
    file_type = data.filename.split('.')[-1]
    if file_type in allowed_file_types:
        if file_type =='tsv':
            content = pl.read_csv(data, sep='\t')
        else:
            content = pl.read_csv(data)
        if set(columns).issubset(content.columns):
            error = ''
        else:
            content = pl.DataFrame()
    return error, content

def validate(data, type):

    if type == "userCls":
        allowed_file_types = ['csv']
        columns = ['Function','Subsystem', 'System', 'Category']
        error = 'Неверный формат пользовательской классификации'

    if type == "rastDownload":
        allowed_file_types = ['csv', 'tsv']
        columns = ['Function','Subsystem']
        error = 'Неверный формат выгрузок из RAST'

    if type == "breakdown":
        allowed_file_types = ['csv']
        columns = ['Strain','Breakdown Type']
        error = 'Неверный формат разбивки данных'

    return template(allowed_file_types, data, columns, error)


def validate_tree(tree_file, otu_file):
    tree=""
    otu_ids=""
    errors=[]
    if tree_file.split('.')[-1] == "txt":
        with open(tree_file) as f:
            tree_contents = f.read()
        tree = TreeNode.read(StringIO(tree_contents))
    else:
        errors.append("неверный формат дерева")

    if otu_file.split('.')[-1] == "txt":
        with open(otu_file) as f:
            otu_ids_contents = f.read()
        otu_ids = re.sub("['|\n|' '|$|&|?]", "", otu_ids_contents).split(",")
    else:
        errors.append("неверный формат otu_ids")

    return errors, tree, otu_ids



