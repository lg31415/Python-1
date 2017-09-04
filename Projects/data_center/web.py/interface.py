import os
import sys
import web
import logging
#web.config.debug = False

sys.path.append("./conf")
sys.path.append("./pycomm")
sys.path.append("./welcome")
sys.path.append("./data_center")

import utility

urls = (
    '/','welcome.Handler',
    '/dc','data_center.Handler',
    )

app = web.application(urls, globals(), autoreload=True)
#app.config['debug'] = False
utility.init_logger("log/interface.log")
log = logging.getLogger('root')
log.info('Loading interface.py')

if __name__ == '__main__':
    app.run()#debug = False)
else:
    application = app.wsgifunc()
