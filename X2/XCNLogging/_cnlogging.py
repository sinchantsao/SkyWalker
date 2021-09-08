# coding=utf8
__author__ = 'caoxingcheng'

import typing
import threading

from . import loglevel
from .util import _where_is_log, LoggerManager, LogFormat,\
                  OutHandler, LevelOutHandler
from ..utlis import blank, serialize, create_dir

_WLocker = threading.RLock()
_CLocker = threading.RLock()


class CNLogging(LogFormat):

    def __new__(cls, name='X2', outers=None):
        # 用户如果没有主动调用init将采用默认形式初始化
        if not LogFormat._share_:
            LogFormat.init()

        ins = super(CNLogging, cls).__new__(cls)
        # 每一个创建的实例都将采用LoggerManager统一管理，避免重复实例化
        LoggerManager.register(name, ins)
        return ins

    def __init__(self, name='X2', outers=None):
        # type: (str, typing.Dict[typing.AnyStr, OutHandler]) -> None
        super(CNLogging, self).__init__()

        self.__dict__ = LogFormat._share_

        # OUTERS属性为`LogFormat._share_`当中共享而来
        if isinstance(outers, dict):
            self.OUTERS.update(outers)

        self.logname = name

    # def _linesStrategy(self):
    #     if self._writeLineCount > self.MAX_LINE:
    #         self._fileout = open(LogFormat.formatFilename(), 'w')
    #         self._writeLineCount = 0
    #     self._writeLineCount += 1
    #
    # def _dateStrategy(self):
    #     d = datetime.datetime.now().strftime('%Y%m%d')
    #     if d != self._dateRef:
    #         self._fileout = open(LogFormat.formatFilename(), 'w')
    #         self._dateRef = d

    def _splicing(self, where, levelname, pstring):
        return self._share_[self._sLOG_FMT].format(
            logname=self.logname,
            where=where,
            levelname=levelname,
            pstring=pstring
        ) + '\n'

    def removeOuter(self, outername):
        try:
            self.OUTERS.pop(outername)
            return True, outername
        except KeyError:
            return False, outername

    def log(self, level, loginfo, where=None, dist=None, cache=False, flush=True):
        # type: (int, typing.Any, str, typing.Dict[typing.AnyStr, typing.Dict[str, bool]], bool, bool) -> None
        """
        @dist 不配置dist则默认所有Outer都进行写入, 不进行缓存一次性输出
              配置规范为{ Outer-name : { flush: bool, cache: bool }, ... }
              不配置的则采用参数cache/flush作为默认
        """

        where = where or _where_is_log()
        levelname = loglevel.LEVEL_NAMES[level]
        loginfo = serialize(loginfo)
        loginfo = self._splicing(where=where, levelname=levelname, pstring=loginfo)

        if dist is None:
            outernames = self.OUTERS.keys()
            dist = {}
        else:
            outernames = dist.keys()

        for out in outernames:
            outer = self.OUTERS.get(out, blank)
            if dist.get(out, {}).get('cache', cache):
                outer.cache()
            else:
                outer.write(loginfo, level)
            if dist.get(out, {}).get('flush', flush):
                outer.flush()

    def logright(self, level, loginfo, where=None):
        self.log(level, loginfo, _where_is_log(), where, False, True)

    def debug(self, loginfo, dist=None, cache=False, flush=True):
        self.log(level=loglevel.DEBUG, loginfo=loginfo, where=_where_is_log(),
                 dist=dist, cache=cache, flush=flush)

    def warn(self, loginfo, dist=None, cache=False, flush=True):
        self.log(level=loglevel.WARN, loginfo=loginfo, where=_where_is_log(),
                 dist=dist, cache=cache, flush=flush)

    def info(self, loginfo, dist=None, cache=False, flush=True):
        self.log(level=loglevel.INFO, loginfo=loginfo, where=_where_is_log(),
                 dist=dist, cache=cache, flush=flush)

    def fatal(self, loginfo, dist=None, cache=False, flush=True):
        self.log(level=loglevel.FATAL, loginfo=loginfo, where=_where_is_log(),
                 dist=dist, cache=cache, flush=flush)

    def error(self, loginfo, dist=None, cache=False, flush=True):
        self.log(level=loglevel.ERROR, loginfo=loginfo, where=_where_is_log(),
                 dist=dist, cache=cache, flush=flush)

    warning = warn
    critical = fatal

