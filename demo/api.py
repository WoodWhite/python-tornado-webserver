# -*- coding: utf-8 -*-
import sys
import json
from os.path import dirname, abspath, join
sys.path.append(dirname(dirname(abspath(__file__))))
from demo.db.models import initialize

import tornado
import tornado.web
from tornado.options import define, options

from api.people import PeopleHandler


define('host', default='0.0.0.0', help='run on the given host', type=str)
define('port', default=8005, help='run on the given port', type=int)


def set_dbSession(db_conf):
    with open(db_conf, 'r') as f:
        db_conf = json.load(f)
    host = db_conf.get('host', '127.0.0.1')
    port = db_conf.get('port', '3306')
    user = db_conf.get('user', '')
    password = db_conf.get('password', '')
    db_name = db_conf.get('db', '')
    return initialize(host, port, user, password, db_name)


def main():
    BASE_DIR = dirname(abspath(__file__))
    db_conf = join(BASE_DIR, 'etc/db.conf')
    settings = dict(
        debug=False,
        dbSession=set_dbSession(db_conf),
    )

    tornado_conf = join(BASE_DIR, 'etc/api.conf')
    tornado.options.parse_config_file(tornado_conf)
    tornado.options.parse_command_line()
    print 'Log Handlers: %s' % tornado.log.logging.getLogger().handlers

    application = tornado.web.Application([
        (r'/xxx/v1/people', PeopleHandler),
        (r'/xxx/v1/people/(\w+)', PeopleHandler),
    ], **settings)

    application.listen(options.port, options.host)
    print 'delaylive server running on %s:%s' % (options.host, options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
