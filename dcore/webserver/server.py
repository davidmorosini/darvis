import sys
import threading
import logging
import socketserver

from shandler import Shandler
from constants import WEBSERVER, WEBSERVICE_HOST, WEBSERVICE_PORT


class Webserver(threading.Thread):
    def __init__(self, configs):
        threading.Thread.__init__(self)
        self.configs = configs
        self.threads = {
            'bot':[]
        }


    def run(self):
        server_class = socketserver.TCPServer
        webservice = server_class((self.configs[WEBSERVER][WEBSERVICE_HOST], self.configs[WEBSERVER][WEBSERVICE_PORT]), Shandler)
        logging.info('svision webserver starts - %s:%s' % (self.configs[WEBSERVER][WEBSERVICE_HOST], self.configs[WEBSERVER][WEBSERVICE_PORT]))
        try:
            print('svision webserver starts in localhost:' + str(self.configs[WEBSERVER][WEBSERVICE_PORT]))
            webservice.serve_forever()
        except KeyboardInterrupt:
            logging.info('svision webserver stop by manual action')
        except: 
            raise
            logging.info("Unexpected error, svision webserver stops because: %s" % (sys.exc_info()))

        webservice.server_close()
        logging.info('svision webserver stops - %s:%s' % (self.configs[WEBSERVER][WEBSERVICE_HOST], self.configs[WEBSERVER][WEBSERVICE_PORT]))

    
