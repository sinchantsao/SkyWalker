# coding=utf8
__author__ = 'caoxingcheng'

import pandas
import tempfile
import typing
import xlrd
import zipfile
import logging
from collections import OrderedDict
from copy import deepcopy
from xml.etree.ElementTree import ParseError

from X2.XCoding import convert_to_unicode
from X2.XExcel import ERROR_EXCEL, EMPTY_EXCEL

_logger = logging.getLogger(__name__)
_DamagedFileNote = "Reading excel failed, try second solution " \
                   "but meet read error type: {exc_type} one more, " \
                   "this file is probably not a complete file in fact, " \
                   "if this file is important, you'd better check it out."


def read_excel_by_fileflow(fileflow) -> OrderedDict:
    u"""
    @Desc:
        read and format excel data through binary data
    @fileflow:
        raw data <string>
    @Return
        <collections.OrderDict> instance, each sheet name as the key
    """
    if isinstance(fileflow, typing.BinaryIO):
        fileflow = fileflow.read()
    dataframes_map = OrderedDict()
    try:
        with tempfile.TemporaryFile() as tf_handler:
            tf_handler.write(fileflow)
            tf_handler.seek(0)
            sheetsNames = pandas.ExcelFile(tf_handler).sheet_names
            for sheet_name in sheetsNames:
                dataframes_map[sheet_name] = pandas.read_excel(tf_handler,
                                                               header=None,
                                                               sheet_name=sheet_name)
    except UnicodeDecodeError:
        try:
            dataframes_map.clear()
            tabular = pandas.ExcelFile(xlrd.open_workbook(file_contents=fileflow,
                                                          encoding_override="GB18030"),
                                       engine='xlrd')
            sheetsNames = tabular.sheet_names
            for sheet_name in sheetsNames:
                dataframes_map[sheet_name] = pandas.read_excel(tabular,
                                                               header=None,
                                                               sheet_name=sheet_name)
        except (AssertionError, UnicodeDecodeError) as exc:
            dataframes_map = deepcopy(ERROR_EXCEL)
            _logger.warning(_DamagedFileNote.format(exc_type=type(exc)))

    except xlrd.XLRDError:
        try:
            with tempfile.TemporaryFile() as tf_handler:
                tf_handler.write(fileflow)
                tf_handler.seek(0)
                dataframes_map = {'default': pandas.read_csv(tf_handler,
                                                             encoding='GB18030',
                                                             header=None)}
        except UnicodeDecodeError:
            dataframes_map = deepcopy(ERROR_EXCEL)
        except pandas.errors.EmptyDataError:
            dataframes_map = deepcopy(EMPTY_EXCEL)
        except pandas.errors.ParserError:
            dataframes_map = deepcopy(ERROR_EXCEL)
    except (ParseError, zipfile.BadZipfile):
        dataframes_map = deepcopy(ERROR_EXCEL)
    return dataframes_map


def read_excel_by_filepath(filepath) -> OrderedDict:
    u"""
    @Desc:
        read and format excel file data through opening and reading file stored in local filesystem
    @filepath:
        abspath
    @Return:
        <collections.OrderDict> instance, each sheet name as the key
    """
    dataframes_map = OrderedDict()
    try:
        sheets_names = pandas.ExcelFile(filepath).sheet_names
        for sheetName in sheets_names:
            dataframes_map[sheetName] = pandas.read_excel(filepath,
                                                          header=None,
                                                          sheet_name=sheetName)
    except UnicodeDecodeError:
        try:
            tabular = pandas.ExcelFile(xlrd.open_workbook(filename=filepath,
                                                          encoding_override="GB18030"),
                                       engine='xlrd')
            sheets_names = tabular.sheet_names
            for sheetName in sheets_names:
                dataframes_map[sheetName] = pandas.read_excel(tabular,
                                                              header=None,
                                                              sheet_name=sheetName)
        except (AssertionError, UnicodeDecodeError) as exc:
            dataframes_map = deepcopy(ERROR_EXCEL)
            _logger.warning(_DamagedFileNote.format(exc_type=type(exc)))

    except xlrd.XLRDError:
        try:
            dataframes_map.clear()
            dataframes_map['default'] = pandas.read_csv(filepath,
                                                        encoding='GB18030',
                                                        header=None)
        except pandas.errors.EmptyDataError:
            dataframes_map = deepcopy(EMPTY_EXCEL)
        except pandas.errors.ParserError:
            with open(filepath, mode='r') as handler:
                dataframes_map['default'] = pandas.DataFrame([convert_to_unicode(line)
                                                              for line in handler])
        except UnicodeDecodeError as exc:
            _logger.warning(_DamagedFileNote.format(exc_type=type(exc)))
            dataframes_map = deepcopy(ERROR_EXCEL)
    except (ParseError, zipfile.BadZipfile) as exc:
        _logger.warning(_DamagedFileNote.format(exc_type=type(exc)))
        dataframes_map = deepcopy(ERROR_EXCEL)
    return dataframes_map
