# coding=utf8

import re
import traceback
import warnings
from inspect import getfullargspec
from collections import OrderedDict
from Stock.exchange import dtypes
from X1.stand import ArgStandError


class Action:

    def __init__(self,
                 action: callable,
                 name: str,
                 dest: dtypes.StockData,
                 must_return: bool = True,
                 priority: int = 0):
        """

        Args:
            action:  可执行函数(参数必须大于0)/方法(参数必须大于1)/对象(参数必须大于0)
            name: 行为名称
            dest(dtypes.StockData): 目标数据
            must_return(bool): 是否必须返回数据
            priority: 权重优先
        """
        if not self._legal_action(action):
            raise ArgStandError(
                "argument `action` should be a callable and arguments length > 1 if it's regular function, "
                "but 2 and even more arguments are required when it's a method by someone instance(because of self)")
        self.name = name
        self.dest = dest
        self.must_return = must_return
        self.priority = priority
        self._run = action

    @staticmethod
    def _legal_action(action):
        """ 注册action的合法性检查 """
        if not callable(action):
            return False
        args_detail = getfullargspec(action)
        args_length = len(args_detail.args)
        conditions = (args_length > 1,
                      args_length > 0 and args_detail.args[0] != 'self',
                      args_detail.varargs)
        return any(conditions)

    def __call__(self, *args, **kwargs):
        self._run(*args, **kwargs)


class Event(object):
    """
    Event 用于管理数据采集行为事件,每创建一个 Event 对象都应该被注册到 EventManage 事件管理对象中;

    数据采集过程中会根据 Event 对象状态进行采集数据,从触发执行事件起(running 为 True),每次数据采
    集时 action(s) 会逐一被调用执行;

    当事件结束时,被注册到事件管理对象中的事件对象会被自动注销,注销前事件管理对象会先取出事件中采集保
    存在容器中的数据,前提是事件对象中为 action(s) 创建了相应的容器,如果是外部传入的容器则需要主动
    介入管理,避免造成采集的数据丢失;

    """

    def __init__(self, name: str, auto_container: bool = True):
        """
        设想之初 running 只设值 True 一次,当设值 True 后将不再改变,而通过 expired 接管状态.
        running 为 True 则表示这个事件已经被激活过了,后续则通过 expired 来了解这个事件是
        否已经结束.
        当 EventManage 对象被注销时,应该管理到 Event 对象的这些状态，当 Event 连 running
        都没有被激活，应该认为是有问题的,即便不报错也应该有警告.

        事件错误管理 errors 和采集容器管理 containers 略微不同,错误管理是针对 actions 来
        进行管理的,而容器管理是针对 actions 的 dest 属性(解析数据归类)来进行管理的.

        Args:
            name: 事件的名称,在同一 EventManage 对象下应该保持唯一.
            auto_container: 是否自动为每个注册的 action 创建处理结果容器.

        """
        self.name = name
        self.auto_container = auto_container
        self.running = False
        self.expired = False
        self.active_triggers = []
        self.deactivate_triggers = []
        self.actions: OrderedDict[dtypes.StockData, [Action]] = OrderedDict()
        self.containers = {}
        self.errors = {}

    @staticmethod
    def __get_action_dest(action):
        return getattr(action, "dest")

    @staticmethod
    def __get_action_name(action):
        return getattr(action, "name")

    def register_active_trigger(self, trigger):
        """
        注册 Event 激活的触发行为
        Args:
            trigger(callable): 可执行对象/函数/方法,返回结果仅有 True/False.

        """

        self.active_triggers.append(trigger)

    def register_deactivate_trigger(self, trigger):
        """
        注册 Event 失效的触发行为
        Args:
            trigger(callable): 可执行对象/函数/方法,返回结果仅有 True/False.

        """

        self.deactivate_triggers.append(trigger)

    def register_action(self, action: Action, container: [list, None] = None):
        """
        在事件对象中注册 action, action 仅在事件 running 属性为 True 时生效,expired 为 True 时失效,
        若事件属性 auto_container 为 True,则注册时相应创建一个行为结果存储列表.

        Args:
            action(callable): 既可以是可执行类实例对象,也可以是函数/方法,但必须包含以下几项属性值:

                - name(str): 由于是通过 dict 管理 action, name 在单一 Event 对象中唯一;

                - must_return(bool): 为了保证行为的处理结果能够按照预期返回结果,即
                                     当事件被触发启用时,行为是否必须返回值;

                - dest(str): 为了管理不同 action 的不同目标数据或相同目标数据,创建统一
                             的采集容器;

                - priority: 为了管理 action 的权重优先采集问题,可以更方便调整采集顺序,
                            在调试和提升效率都有很大帮助;

                同时需要注意的是 action 接受的参数至少>1, 第一个参数为事件对象.

            container(optional[list, set, dict]): 注册action时可以单独为该类action传
                     入指定的container,以便于更多方式的数据存储选择.

        """
        if not isinstance(action, Action):
            raise ArgStandError(f"Arg `action` should be an Action instance not {type(action)}")

        if action.dest not in self.actions:
            self.actions[action.dest] = []
        self.actions[action.dest].append(action)
        # sort action by priority of action, the smaller the higher the priority
        self.actions[action.dest].sort(key=lambda a: a.priority)

        if container is not None:
            adopt_method = getattr(container, "append", None)
            if not (callable(adopt_method) and getfullargspec(adopt_method).args == 2):
                raise ArgStandError(f"<{container}> is not an expected 'Container type', 'Container type' has to have "
                                    f"a method `append` for adopting, you can inherit from list or custom yourself.")
            if action.dest in self.containers:
                del self.containers[action.dest]
                warnings.warn("Original container is replaced by custom container, "
                              "recommend is custom container firstly and only once for the same destination.")

        elif self.auto_container is True:
            self.register_container(action.dest, __inside=True)

    def register_container(self, __dest, /, *, __inside=False):
        if not isinstance(__dest, str):
            __dest = self.__get_action_dest(__dest)

        if __dest not in self.actions:
            self.containers[__dest] = []
        elif not __inside:
            warnings.warn("Container register once only, no necessary to register twice more for the same destination")

    def __call__(self, *args, **kwargs):
        """
        Event对象作为被调用对象使用,在数据采集过程中最小单位数据遍历一次即调用一次,根据Event对象
        状态做出相应处理.
        使用Event对象必须外部控制Event过期状态(由于Event一般被注册到EventManage中进行管理,即
        这里所指的`外部`一般指EventManage的封装当中),当Event对象过期(expired为True)将不能再使用.

        action管理是通过其自身的dest属性归类成list放置在dict中,而相同dest的action在list中会根据
        authority属性权重来进行排序,数据的的采集也会以此为先后顺序,一旦存在action采集到数据,后续的
        action将不会再执行.

        Args:
            Event对象在创建期间就对所有行为进行了封装,当Event对象被调用时,传入的参数均为需要被采集的必要数据

        """

        if self.expired is True:
            raise RuntimeError("Event has expired!")

        if self.running is False:
            if any(trigger(*args, **kwargs) for trigger in self.active_triggers):
                self.running = True

        if self.running is True:
            for dest, actions in self.actions.items():
                catchone = False
                for action in actions:
                    result = None
                    try:
                        # 为了能够更加精确把控行为,将事件也传入行为处理中
                        result = action(self, *args, **kwargs)
                    except (Exception,):
                        exc = traceback.format_exc()
                        name = action.name
                        self.errors[name] = exc
                    if result is not None:
                        catchone = True
                        if dest in self.containers:
                            self.containers[dest].append(result)
                    if catchone is True:
                        break


class EventManage:

    def __init__(self):
        self.events = dict()
        self.errors = dict()
        self.results = dict()

    def register(self, event, /, *args, **kwargs):
        __event = getattr(event, 'name')
        self.events[__event] = (event, args, kwargs)
        self.errors[__event] = None
        self.results[__event] = None

    def unregister(self, __event):
        if isinstance(__event, Event):
            __event = getattr(__event, 'name')
        try:
            self.events.pop(__event)
            self.errors.pop(__event)
            self.results.pop(__event)
        except KeyError:
            raise KeyError(f"event <{__event}> was not registered")

    def run(self):
        for __event, (action, args, kwargs) in self.events.items():
            self.results[__event] = None
            try:
                self.results[__event] = action(*args, **kwargs)
            except Exception:
                exc = traceback.format_exc()
                self.errors[__event] = exc


def deliver_regex(pattern, rawdata):
    """
    将正则表达式和需要匹配的数据进行传递,返回匹配结果
    Args:
        pattern: 正则表达式,正则表达式必须保证被匹配数据都带有命名空间
        rawdata: 被匹配数据

    Returns:
        - 无数据:None
        - 有数据:dict
    """
    if "(?P<" not in pattern:
        raise ValueError(f"can not find namespace in pattern '{pattern}'")
    regex = re.compile(pattern)
    result = regex.search(rawdata)
    if result is not None:
        return result.groupdict()
    return result


def pick_by_space():
    pass
