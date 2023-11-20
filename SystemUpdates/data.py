from Tools.FetchData import ReturnQsList, document_queryset, fetch_cm_data_from_model_def
from settings import DEV_ID, LEVEL


def make_queryset_documentation(level:str=LEVEL, dev_id:str=DEV_ID):
    qslist = ReturnQsList(level)
    document_queryset(qslist, dev_id)


def get_data(level:str="cm"):
    qslist = ReturnQsList(level)
    datasets= fetch_cm_data_from_model_def(qslist)
    return datasets



