# coding=utf8
__author__ = 'caoxingcheng'

import datetime
import inspect
import os
import sys
import threading
from . import loglevel
from X2.utlis import create_dir


class LogFormat(object):
    
    _share_ = {}
    
    _sMAX_LINE           = 'MAX_LINE'
    _sFILE_TAG           = 'FILE_TAG'
    _sFILE_TFM           = 'FILE_TFM'
    _sLOG_TFM            = 'LOG_TFM'
    _sLOG_FMT            = 'LOG_FMT'
    _sLOG_PATH           = 'LOG_PATH'
    _sOuters             = 'OUTERS'
    _sLOGFILE_STRA       = 'LOGFILE_STRA'
    _sCORDON_OUT_LV      = 'CORDON_OUT_LV'
    _sDEFAULT_OUT_LV     = 'DEFAULT_OUT_LV'
    _sFileOutPointer     = 'FileOutPointer'
    _sConsoleOutPointer  = 'ConsoleOutPointer'

    MAX_LINE = 5000000

    FILE_TAG = 'X2'
    FILE_TFM = '%Y-%m-%d_%H:%M:%S'
    LOG_TFM  = '%Y-%m-%d_%H:%M:%S'
    LOG_FMT  = '{logname:<5} {where:<15} {levelname:<8} {pstring}'

    CORDONOUT_LV  = loglevel.FATAL
    DEFAULTOUT_LV = loglevel.DEFAULT
    
    OUTERS = {}

    LOG_PATH = '/tmp/X2_logs/'

    def __init__(self):
        self.__dict__ = LogFormat._share_

    @staticmethod
    def init(**kwargs):
        """
        该类所属域下的`setXXXX`方法都应该在该方法之前进行调用,该方法所有的设值参数都基于默认设值或其他`setXXXX`方法设值
        该方法在CNLogging创建对象之前将会被调用,进行初始化`LogFormat._share_`,
        而CNLogging当中每一个对象的__dict__都被重新定向到`LogFormat._share_`属性,从而享元

        @MAX_LINE           弃用了没卵用,本来用来统计日志到达多少内容就换文件的

        @FILE_TAG           log文件名称的格式请参考本属类formatFilename方法,而该参数用于文件名前缀标识

        @FILE_TFM           log文件名称的格式请参考本属类formatFilename方法,而该参数用于生成文件名中的时间部分格式

        @LOG_TFM            日志内容的时间输出格式

        @LOG_FMT            log日志内容的格式形式,log格式是通过字符串format形式生成的,传递三个参数:
                                - logname  : 日志对象名称
                                - where    : 日志产生于哪里
                                - levelname: 日志输出等级
                                - pstring  : 日志数据，具体数据长啥样请参考

        @LOG_PATH           存放log数据的目录

        @OUTERS             详细阅读OutHandler代码,该参数为一个dict形式

        @LOGFILE_STRA       弃用了没卵用,本来用来设计日志文件切换文件的方式设置
        @CORDON_OUT_LV      弃用了没卵用
        @DEFAULT_OUT_LV     弃用了没卵用,本来用来设置标准输出等级
        @FileOutPointer     弃用了没卵用,本来用来设置文件日志输出的存储成员,现在的设计结构来说这玩意儿弱爆了
        @ConsoleOutPointer  弃用了没卵用, 同上@FileOutPointer

                              ↗      ↖

                            没卵用的为啥没删除？因为我也不知道以后还会不会重新启用，永远在重构
        """
        outers = kwargs.pop(LogFormat._sOuters, {'default': OutHandler(sys.stdout)})
        LogFormat.setOuters(outers)
        settings = {
            LogFormat._sOuters  : LogFormat.OUTERS,
            LogFormat._sMAX_LINE: LogFormat.MAX_LINE,
            LogFormat._sFILE_TAG: LogFormat.FILE_TAG,
            LogFormat._sFILE_TFM: LogFormat.FILE_TFM,
            LogFormat._sLOG_TFM : LogFormat.LOG_TFM,
            LogFormat._sLOG_PATH: LogFormat.LOG_PATH,
            LogFormat._sLOG_FMT : LogFormat.LOG_FMT,
            LogFormat._sCORDON_OUT_LV    : LogFormat.CORDONOUT_LV,
            LogFormat._sDEFAULT_OUT_LV   : LogFormat.DEFAULTOUT_LV,
            LogFormat._sConsoleOutPointer: sys.stdout,
        }
        outreq = set(kwargs.keys()) - set(settings.keys())
        if outreq:
            raise ValueError('unexpected params: %s' % list(outreq))
        settings.update(kwargs)
        create_dir(settings[LogFormat._sLOG_PATH])
        # 所有的共享参数都放入_share_当中，而实例__dict__重新赋值为_share_，每一个实例都将共享统一配置
        LogFormat._share_.update(settings)
        return settings

    @staticmethod
    def formatFilename():
        return '{filetag}_{filetmf}.log'.format(filetag=LogFormat.FILE_TAG,
                                                filetmf=datetime.datetime.now().strftime(LogFormat.FILE_TFM))

    @staticmethod
    def setLogpath(path):
        """ 日志存放位置 """
        LogFormat.LOG_PATH = path

    @staticmethod
    def setLogTfm(fmt):
        # type: (str) -> None
        """ 日志内容输出时间格式 """
        LogFormat.LOG_TFM = fmt

    @staticmethod
    def setFileTfm(fmt):
        # type: (str) -> None
        """ 日志文件名当中的时间数据格式 """
        LogFormat.FILE_TFM = fmt

    @staticmethod
    def setFileTag(tag):
        # type: (str) -> None
        """ 日志文件名当中的前缀标识 """
        LogFormat.FILE_TAG = tag

    @staticmethod
    def setCordon(lv):
        # type: (int) -> None
        """ 弃用了没卵用 """
        LogFormat.CORDONOUT_LV = lv

    @staticmethod
    def setDefaultOut(lv):
        # type: (int) -> None
        """ 弃用了没卵用 """
        LogFormat.DEFAULTOUT_LV = lv

    @staticmethod
    def setOuters(outers):
        """
        @outer  outers应该是个字典集合,每一个outer都有自己的所属key名称,以便于管理
                outer即为类`OutHandler`及其子类所创建的对象
        """
        LogFormat.OUTERS.update(outers)


class LoggerManager:
    _Pool = {}

    def __init__(self):
        self.__dict__ = LoggerManager._Pool

    @staticmethod
    def register(name, instance):
        LoggerManager._Pool[name] = instance


class OutHandler(object):

    def __init__(self, file):
        self._lock = threading.RLock()
        if isinstance(file, str):
            if file.startswith(('./', '../')):
                file = os.path.abspath(file)
            if not os.path.isabs(file):
                file = os.path.join(LogFormat.LOG_PATH, file)
            self.file = open(file, 'w')
        else:
            self._file = file
        self._cache = []

    def cache(self, msg, level=None):
        self._cache.append(msg)

    def close(self):
        self._file.close()

    def write(self, msg, level=None):
        with self._lock:
            self._file.write(msg)

    def flush(self):
        with self._lock:
            for line in self._cache:
                self._file.write(line)
            self._file.flush()


class LevelOutHandler(OutHandler):
    def __init__(self, file, level=None, levels=None):
        super(LevelOutHandler, self).__init__(file)
        self._level  = 0 if level is None else level
        self._levels = [] if levels is None else levels

    def cache(self, msg, level=None):
        if level == self._level or level in self._levels:
            self._cache.append(msg)

    def write(self, msg, level=None):
        if level == self._level or level in self._levels:
            with self._lock:
                self._file.write(msg)

    def flush(self):
        with self._lock:
            for line in self._cache:
                self._file.write(line)
            self._file.flush()


def getLogger(name='X2', outers=None):
    from ._cnlogging import CNLogging
    return LoggerManager._Pool.get(name, CNLogging(name=name, outers=outers))


def _where_is_log():
    return inspect.stack()[2][3]
