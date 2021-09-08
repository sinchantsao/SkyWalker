# coding=utf8

from sqlalchemy.orm import Session

class BlueprintPro(object):

    def __init__(self, name):
        self.name = name.strip('/')
        self.mounter = []

    def route(self, rule, **options):
        def decorator(view_func):
            self.mounter.append((view_func, rule, options))
            return view_func
        return decorator

    def register(self, blueprint, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for view_func, rule, options in self.mounter:
            endpoint = options.pop('endpoint', view_func.__name__)
            blueprint.add_url_rule(url_prefix + rule, endpoint, view_func, **options)

