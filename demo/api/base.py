# -*- coding: utf-8 -*-
import json

from tornado.web import RequestHandler

UNKNOW_ERROR = 2333
MSG = ''


class BaseHandler(RequestHandler):

    def initialize(self):
        self.code = UNKNOW_ERROR
        self.msg = MSG
        self.data = {}
        self.session = self.settings.get('dbSession')()

    def on_finish(self):
        self.session.close()

    def _response(self):
        res = {}
        res['Code'] = self.code
        res['Msg'] = self.msg
        res.update(self.data)
        res = str(json.JSONEncoder().encode(res)).encode('utf-8')
        self.write(res)
