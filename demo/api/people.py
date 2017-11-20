# -*- coding: utf-8 -*-
import json

from tornado import gen
import logging as log
from sqlalchemy import and_

from base import BaseHandler
from decorator import xxx_auth, xxx_except
from demo.db.models import People

CREATE_PEOPLE_OK = 1005
CREATE_PEOPLE_ERROR = 2005
CANCEL_PEOPLE_OK = 1006
CANCEL_PEOPLE_ERROR = 2006
GET_PEOPLE_OK = 1008
GET_PEOPLE_ERROR = 2008
DELETE_PEOPLE_OK = 1009
DELETE_PEOPLE_ERROR = 2009


class PeopleHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET', 'POST', 'PUT', 'DELETE')

    @gen.coroutine
    @xxx_except(CREATE_PEOPLE_ERROR, 'CREATE_PEOPLE_ERROR')
    @xxx_auth(CREATE_PEOPLE_ERROR)
    def post(self):

        def check_args(name):
            if not (name and
                    isinstance(name, str)):
                return False
            return True

        self.code = CREATE_PEOPLE_OK
        data = json.loads(self.request.body.decode('utf8'))
        name = data.get('name', None)

        if not check_args(name):
                self.code = CANCEL_PEOPLE_ERROR
                self.msg = 'Name %s error!' % name
                log.info('[code: %d] CREATE_PEOPLE_ERROR by %s'\
                    % (self.code, self.msg))
                self.set_status(400)
                self._response()

        query = self.session.query(People)\
            .filter(People.name == name)\
            .all()
        if len(query) == 0:
            new_people = People(
                name = name
            )
            self.session.commit()
        else:
            new_people = query[0]

        self.data['id'] = new_people.id
        log.info('[code: %d] CREATE_PEOPLE_OK body{%s}'\
            % (self.code, ''.join(self.request.body.split())))
        self._response()


    @gen.coroutine
    @xxx_except(GET_PEOPLE_ERROR, 'GET_PEOPLE_ERROR')
    @xxx_auth(GET_PEOPLE_ERROR)
    def get(self, *args):

        def single_people(id):
            return

        def all_people(limit, page, state, start, end):
            return

        self.code = GET_PEOPLE_OK
        if args:
            peopleId = args[0]
            res = single_people(peopleId)
            if not res:
                self.code = GET_PEOPLE_ERROR
                self.msg = 'Can not find people %s!' % peopleId
                log.info('[code: %d] GET_PEOPLE_ERROR by %s'\
                    % (self.code, self.msg))
                self.set_status(400)
            log.info('Query single people %s', peopleId)
        else:
            limit = int(self.get_argument('Limit', 20))
            page = int(self.get_argument('Page', 1))
            state = self.get_argument('State', None)
            start = self.get_argument('Start', None)
            end = self.get_argument('End', None)
            res = all_people(limit, page, state, start, end)
            log.info('Query all file people')
        self.data = res
        self._response()

    @gen.coroutine
    @xxx_except(CANCEL_PEOPLE_ERROR, 'CANCEL_PEOPLE_ERROR')
    @xxx_auth(CANCEL_PEOPLE_ERROR)
    def put(self):

        def check_args(id, state):
            if not():
                return False
            return True

        self.code = CANCEL_PEOPLE_OK
        data = json.loads(self.request.body.decode('utf8'))
        people_id = data.get('Id')
        state = data.get('State')
        if not check_args(people_id, state):
            self.code = CANCEL_PEOPLE_ERROR
            log.info('[code: %d] CANCEL_PEOPLE_ERROR body{%s} by %s'\
                % (self.code, ''.join(self.request.body.split()), self.msg))
            self.set_status(400)
            self._response()
            return

        people = self.session.query(People)\
            .filter(and_(
                People.id==people_id,
                People.state=='Init'
            )).first()
        if not people:
            self.code = CANCEL_PEOPLE_ERROR
            self.msg = 'Can not find people %s!' % people_id
            log.info('[code: %d] CANCEL_PEOPLE_ERROR body{%s} by %s'\
                % (self.code, ''.join(self.request.body.split()), self.msg))
            self.set_status(400)
        elif people.state == state:
            self.msg = 'people %s state already been %s!' %(people_id, state)
            log.info('[code: %d] CANCEL_PEOPLE_ERROR body{%s} by %s'\
                % (self.code, ''.join(self.request.body.split()), self.msg))
            self.set_status(400)
        else:
            people.state = state
            self.session.commit()
            log.info('[code: %d] CANCEL_PEOPLE_OK body{%s}'\
                % (self.code, ''.join(self.request.body.split())))
        self._response()

    @gen.coroutine
    @xxx_except(DELETE_PEOPLE_ERROR, 'DELETE_PEOPLE_ERROR')
    @xxx_auth(DELETE_PEOPLE_ERROR)
    def delete(self, _id):

        self.code = DELETE_PEOPLE_OK
        people = self.session.query(People)\
            .filter(People.id==_id).first()

        if not people:
            self.code = DELETE_PEOPLE_ERROR
            self.msg = 'Can not find people %s!' % _id
            log.info('[code: %d] DELETE_PEOPLE_ERROR %s by %s' %
                     (DELETE_PEOPLE_ERROR, _id, self.msg))
            self.set_status(400)
        else:
            self.session.delete(people)
            self.session.commit()
            log.info('[code: %d] DELETE_PEOPLE_OK %s' %
                     (self.code, _id))
        self._response()
