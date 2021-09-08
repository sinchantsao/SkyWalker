# coding=utf8
__author__ = 'caoxingcheng'

import pandas
from collections import OrderedDict

EMPTY_EXCEL = OrderedDict({'default': pandas.DataFrame()})
ERROR_EXCEL = OrderedDict()
EMPTY_EXCEL.error = False
ERROR_EXCEL.error = True
