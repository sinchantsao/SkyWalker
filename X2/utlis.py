# coding=utf8

__all__ = [
    'SettingTree',
    'serialize',
    'Empty',
    'blank',
    'create_dir',
    'union_date_tuple',
    'gen_date_regex',
    'get_file_ext',
    'CompFileMemFree',
    'get_cur_second',
    'get_cur_microsecond',
    'get_cur_millisecond',
    'read_from_yaml',
    'read_from_ini',
    'wait_child_process'
]

import copy
import datetime
import errno
import logging
import os
import rarfile
import re
import shutil
import signal
import tempfile
import time
import typing as t
import zipfile
from collections import OrderedDict
from inspect import getfullargspec
from io import BytesIO
from six import text_type
from contextlib import contextmanager
from X1.stand import MethodStandError, ParamStandError
from X1.run import UnexpectedCompatible, RetryException
from X1.support import SysSupport

DEFAULT_GLOBAL_NAME = 'GlobalSettings'

_logger = logging.getLogger(__name__)


def serialize(data=""):
    u"""
    序列化数据，主要用于日志输出
    """
    if isinstance(data, dict):
        sets = ["".join([serialize(k), ":", serialize(v), ","]) for k, v in sorted(data.items(), key=lambda x: x[0])]
        dict_content = "".join(sets)
        return "".join(["{", dict_content[:-1], "}"])
    elif isinstance(data, set):
        set_str = ",".join([serialize(i) for i in data])
        return "".join(["{", set_str, "}"])
    elif isinstance(data, list):
        set_str = ",".join([serialize(i) for i in data])
        return "".join(["[", set_str, "]"])
    elif isinstance(data, tuple):
        set_str = ",".join([serialize(i) for i in data])
        return "".join(["(", set_str, ")"])
    elif isinstance(data, (float, int)):
        return str(data)
    elif isinstance(data, str):
        if data:
            return "".join(["'", data, "'"])
        else:
            return "''"
    elif isinstance(data, text_type):
        return "".join(["'", data.encode('utf8'), "'"])
    else:
        return "".join(["'", str(data), "'"])


class Empty(object):

    @classmethod
    def _do_nothing(cls, *args, **kwargs):
        pass

    def __setattr__(self, key, value):
        pass

    def __getattribute__(self, item):
        return Empty._do_nothing

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        return None

    def __index__(self):
        return 0

    def __call__(self, *args, **kwargs):
        self._do_nothing(*args, **kwargs)

    def __nonzero__(self):
        return False

    def __cmp__(self, other):
        return False

    def __str__(self):
        return ''

    def __len__(self):
        return 0

    def __contains__(self, item):
        return False

    def __getslice__(self, start, end):
        return []

    __repr__ = __str__


blank = Empty()  # 用于各种空操作


def create_dir(path: str, chmod: int = 488):
    path = os.path.abspath(path)
    if os.path.isdir(path):
        os.chmod(path, chmod)
        return path
    try:
        os.mkdir(path, chmod)
    except OSError:
        if os.system('mkdir -p %s' % path) != 0:
            raise SysSupport("Failed to create directory `{}`".format(path))
    os.chmod(path, chmod)
    return path


def get_file_ext(file: str, keepraw: bool = True):
    ext = os.path.splitext(file)[-1]
    return ext if keepraw else ext.lower()


def union_date_tuple(date):
    u"""
    一般用于通过日期正则(可参考函数`gen_date_reg`)匹配得出的结果(YYYY, mm, dd)
    对于年/月/日有一定的限制,年必须满足四位数,单数月份前方会进行补零,单数日前方会进行补零
    对于符合基本限制的日期数据最后进行拼接得到`YYYYmmdd`格式的字符串日期数据
    """
    y = m = d = None

    if len(date[0]) == 4:
        y = date[0]

    if len(date[1]) == 1:
        m = '0' + date[1]
    elif len(date[1]) == 2:
        m = date[1]

    if len(date[2]) == 1:
        d = '0' + date[1]
    elif len(date[2]) == 2:
        d = date[2]

    if None in (y, m, d):
        return

    return str("".join((y, m, d)))


def gen_date_regex(start_year: int = 2015):
    u"""
    返回一个用于匹配日期数据的正则对象,该正则对象用于匹配近 start_year 年至今
    """
    this_year = datetime.datetime.today().year
    hn = this_year - start_year + 2
    recent_years = tuple(range(start_year, this_year + 2))

    split_tag = u"\\D{0,3}"  # 0 -> 3 word(s)
    # start_tag = u"\\D*"          # start of cannot be a number
    # end_tag   = u"\\D*$"         # end of cannot be a number

    years_tags = u"(" + (u"|".join([u"%d"] * hn)) + u")"
    years_tags = years_tags % recent_years

    month_tags = u"(0[1-9]|1[0-2]|[1-9])"
    date_tags = u"(0[1-9]|[12]\\d|3[01]|[1-9])"

    rules = split_tag.join((years_tags, month_tags, date_tags))
    REG_DATE = re.compile(rules)

    return REG_DATE


class CompFileMemFree(object):
    """
    解压文件
    """

    # 解压支持文件类型
    _EXTTAG = ('.zip', '.ZIP', '.rar', '.RAR')

    @staticmethod
    def set_rar_executable(path):
        # 设置 rar 解压软件路径, rarfile 库需要依赖于该软件
        # 默认情况下会根据环境命令使用 unrar 命令
        rarfile.UNRAR_TOOL = path

    @staticmethod
    def on(filelike: t.Union[t.TextIO, t.BinaryIO, BytesIO],
           target_ext: t.Union[t.Tuple, str] = None,
           target_files: t.Union[t.List, t.Tuple] = None,
           password: t.ByteString = None) -> t.OrderedDict[str, tempfile.TemporaryFile]:
        """
        通过文件句柄对文件进行解压, 当不希望文件落地时建议采用这种方式
        """
        try:
            return CompFileMemFree.unzip(filelike)
        except zipfile.BadZipfile:
            try:
                return CompFileMemFree.unrar(filelike)
            except rarfile.Error:
                raise UnexpectedCompatible("File is not be compressed.")

    @staticmethod
    def unzip(filelike: t.Union[t.TextIO, t.BinaryIO, BytesIO],
              target_ext: t.Union[t.Tuple, str] = None,
              target_files: t.Union[t.List, t.Tuple] = None,
              password: t.ByteString = None) -> t.OrderedDict[str, tempfile.TemporaryFile]:

        target_fileinfo = set()
        with zipfile.ZipFile(filelike) as zip_handler:
            if any([f.flag_bits & 0x1 for f in zip_handler.filelist]):
                _logger.warning("This file is a encrypted file, CompFileMemFee does not deal with it.")
                return OrderedDict()
            for fileinfo in zip_handler.NameToInfo.keys():
                filename = os.path.split(fileinfo)[-1]
                ext = get_file_ext(fileinfo)
                if target_ext is None and target_files is None:
                    target_fileinfo.add(fileinfo)
                    continue
                if target_files is not None and filename in target_files:
                    target_fileinfo.add(fileinfo)
                if target_ext is not None and ext == target_ext:
                    target_fileinfo.add(fileinfo)

            subfiles_map = OrderedDict()
            for fileinfo in target_fileinfo:
                file_data = zip_handler.getinfo(fileinfo)
                with zip_handler.open(file_data, pwd=password) as source:
                    target = tempfile.TemporaryFile('wb+')
                    shutil.copyfileobj(source, target)
                    target.seek(0, 0)
                subfiles_map[fileinfo] = target
            return subfiles_map

    @staticmethod
    def unrar(filelike: t.TextIO, des_dir: str = '', allow_ext: t.List = None):
        pass
        # subs = []
        #
        # fh = filelike
        # fh.seek(0)
        #
        # with rarfile.RarFile(fh) as rf:
        #     for subfile_info in rf.infolist():
        #         if not subfile_info.isdir():
        #             if subfile_info.needs_password():
        #                 _logger.warning(
        #                     "This is a encrypted compressed file, but FreeCompFile does not support sort of this.")
        #                 return []  # encrypted file
        #             subfile_filename = os.path.split(subfile_info.filename)[-1]
        #             readable_filename = convert_to_unicode(subfile_filename)
        #             subfile_path = os.path.join(des_dir, readable_filename)
        #
        #             if (allow_ext is not None) and (get_file_ext(readable_filename) not in allow_ext):
        #                 continue
        #             with open(subfile_path, 'wb') as subFileHandler:
        #                 shutil.copyfileobj(rf.open(subfile_info), subFileHandler)
        #
        #             subs.append(subfile_path)
        #
        # fh.close()
        #
        # for filepath in subs:
        #     if filepath.endswith(CompFileMemFree._EXTTAG):
        #         subs.remove(filepath)
        #         subfile_obj = open(filepath, 'rb')
        #         subs += CompFileMemFree.on(filelike=subfile_obj)
        # return subs


def get_cur_second(power=0):
    """ 获取当前秒(s) """
    return int(time.time() * pow(10, power))


def get_cur_millisecond():
    """ 获取当前毫秒(ms) """
    return get_cur_second(power=3)


def get_cur_microsecond():
    """ 获取当前微秒(µs) """
    return get_cur_second(power=6)


class SettingTree(dict):
    """
    将dict数据转换成可调用对象形式取数据
    适用于哪些场景？
      1. 不希望看到满屏硬编码;
      2. 对于不确定数据不想进行 try …… catch 捕获 KeyError 异常;
      3. 对于确定字段(key)数据不希望再新增时（freeze机制);
      4. 读取 ya(m)l / ini / cfg 配置文件;
      5. 希望一次配置全局使用，会使用 sys.module 机制全局 import 可用;
    """
    def __init__(__self, *args, **kwargs):
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in kwargs.items():
            __self[key] = __self._hook(val)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError("'SettingTree' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        is_frozen = (hasattr(self, "__frozen") and
                     object.__getattribute__(self, "__frozen"))
        if is_frozen and name not in super(SettingTree, self).keys():
            raise KeyError(name)
        super(SettingTree, self).__setitem__(name, value)
        try:
            p = object.__getattribute__(self, "__parent")
            key = object.__getattribute__(self, "__key")
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, "__parent")
            object.__delattr__(self, "__key")

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __missing__(self, name):
        if object.__getattribute__(self, "__frozen"):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                    (not isinstance(self[k], dict)) or
                    (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def __or__(self, other):
        if not isinstance(other, (SettingTree, dict)):
            return NotImplemented
        new = SettingTree(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, (SettingTree, dict)):
            return NotImplemented
        new = SettingTree(other)
        new.update(self)
        return new

    def __ior__(self, other):
        self.update(other)
        return self

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def freeze(self, should_freeze=True):
        object.__setattr__(self, "__frozen", should_freeze)
        for key, val in self.items():
            if isinstance(val, SettingTree):
                val.freeze(should_freeze)

    def unfreeze(self):
        self.freeze(False)

    @staticmethod
    def set_global_settings(settings, settings_name=DEFAULT_GLOBAL_NAME):
        # type: (dict, str) -> SettingTree
        global_settings = SettingTree(settings)
        import sys
        sys.modules[settings_name] = global_settings
        _logger.debug(f"Set a global object instance of config named '{settings_name}'")
        return global_settings

    @staticmethod
    def set_global_by_yaml(path, settings_name=DEFAULT_GLOBAL_NAME):
        settings = read_from_yaml(path)
        return SettingTree.set_global_settings(settings=settings,
                                               settings_name=settings_name)

    @staticmethod
    def set_global_by_conf(path, settings_name=DEFAULT_GLOBAL_NAME):
        # todo
        raise NotImplemented

    @staticmethod
    def set_global_by_ini(path, settings_name=DEFAULT_GLOBAL_NAME):
        settings = read_from_ini(path)
        return SettingTree.set_global_settings(settings=settings,
                                               settings_name=settings_name)


def read_from_yaml(path):
    import yaml
    with open(path, 'r') as yaml_reader:
        return yaml.load(yaml_reader, Loader=yaml.FullLoader)


def read_from_ini(path):
    import configparser
    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(path)
    format = dict()
    d = cfg_parser._sections
    for sec in d:
        format[sec] = dict(cfg_parser._defaults, **d[sec])
        for op in format[sec]:
            if '\n' in format[sec][op]:
                format[sec][op] = [item.replace(',', '').replace(' ', '')
                                   for item in format[sec][op].split('\n')]
        format[sec].pop("__name__", None)
    return format


class TriggerFn:
    def __init__(self, fn, trigger):
        if getfullargspec(fn) == getfullargspec(trigger):
            self.fn = fn
            self.__trigger__ = trigger
        else:
            raise MethodStandError("Params should be the same between function and trigger.")

    def __call__(self, *args, **kwargs):
        if self.__trigger__(*args, **kwargs):
            return self.fn(*args, **kwargs)

    def key(self, args=None):
        if args is None:
            args = getfullargspec(self.fn).args
        return (
            self.fn.__module__,
            self.fn.__class__,
            self.fn.__name__,
            len(args)
        )


class Satisfy:

    def __init__(self, *caps):
        self._fns = OrderedDict()
        for f in caps:
            wrap_func = self.__mask(f)
            self.register(wrap_func)

    @classmethod
    def __mask(cls, __f, /):
        if isinstance(__f, (list, tuple)):
            fn, trigger = __f
            assert getfullargspec(fn) == getfullargspec(trigger)
        elif callable(__f):
            fn, trigger = __f, lambda *args, **kwargs: True
        else:
            raise ParamStandError("Params should be callable instance or "
                                  "one couple of function and trigger")
        return TriggerFn(fn, trigger)

    def register(self, __f, /):
        self._fns[__f.key()] = __f

    def __call__(self, *args, **kwargs):
        for f in self._fns:
            f(*args, **kwargs)


@contextmanager
def execute_time_limit(timeout):
    def signal_handler(signum, frame):
        raise TimeoutError("Timed out of limitation.")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(timeout)
    try:
        yield
    finally:
        signal.alarm(0)


# Define retry util function
def retry(func: t.Callable, max_retry: int = 10, interval: int = 0):
    for retry_times in range(1, max_retry + 1):
        try:
            return func()
        except Exception:
            _logger.info(f"Failed to run {func.__name__}, in retry({retry_times}/{max_retry})")
        time.sleep(interval)
    else:
        raise RetryException(f"Failed at {func.__name__} after {max_retry} retry-times "
                             f"with per {interval}s interval.")


def wait_child_process(signum, frame):
    _logger.info('receive SIGCHLD')
    try:
        while True:
            # -1 表示任意子进程
            # os.WNOHANG 表示如果没有可用的需要 wait 退出状态的子进程，立即返回不阻塞
            cpid, status = os.waitpid(-1, os.WNOHANG)
            if cpid == 0:
                _logger.info('no child process was immediately available')
                break
            exitcode = status >> 8
            _logger.info('child process %s exit with exitcode %s', cpid, exitcode)
    except OSError as e:
        if e.errno == errno.ECHILD:
            _logger.warning('current process has no existing unwaited-for child processes.')
        else:
            raise


if __name__ == '__main__':
    def error():
        raise ValueError

    retry(error, 3, 2)
    # from pprint import pprint
    # pprint(dir(error))

