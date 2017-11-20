# -*- coding: utf-8 -*-

import logging as log


def xxx_except(err_code, code_str):
    def decorator(func):
        def wrapper(self, *args, **kw):
            try:
                func(self, *args, **kw)
            except Exception as e:
                self.code = err_code
                log.error('[code: %d] %s body{%s} by [%s]' %
                          (self.code, code_str,
                           ''.join(self.request.body.split()), e))
                self.set_status(400)
                self._response()
        return wrapper
    return decorator


def xxx_auth(err_code):
    def decorator(func):
        def wrapper(self, *args, **kw):
            auth = self.request.headers.get('auth', '')
            if not(isinstance(auth, str) and auth):
                self.code = err_code
                self.msg = 'Wrong Auth!'
                self.set_status(401)
                self._response()
            else:
                func(self, *args, **kw)
        return wrapper
    return decorator
