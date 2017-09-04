import time, datetime
import logging
from logging.handlers import RotatingFileHandler

#from thrift.transport import TTransport
#from thrift.protocol import TBinaryProtocol, TProtocol

def now_time():
        return time.strftime("%Y%m%d %H:%M:%S", time.localtime())


def init_logger(path, level=logging.NOTSET, maxBytes=100*1024*1024, backupCount=20):
        logger = logging.getLogger()
        logger.setLevel( level )
        file_handler = RotatingFileHandler(path, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setFormatter( logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y%m%d %H:%M:%S") )
        logger.addHandler(file_handler)

def init_logger2(path, level=logging.NOTSET, maxBytes=50*1024*1024, backupCount=20):
        #logger = None
        logger = logging.getLogger()
        logger.setLevel( level )
        file_handler = RotatingFileHandler(path, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.setFormatter( logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y%m%d %H:%M:%S") )
        logger.addHandler(file_handler)
        #return (logger, file_handler)


#def thrift_encode(pack):
#        transport = TTransport.TMemoryBuffer()
#        protocol = TBinaryProtocol.TBinaryProtocol(transport)
#        pack.write(protocol)
#        return transport.getvalue()

#def thrift_decode(value, pack):
#        transport = TTransport.TMemoryBuffer( value )
#        protocol = TBinaryProtocol.TBinaryProtocol(transport)
#        pack.read(protocol)
#        return pack

def suffix(name):
    pos = name.rfind(".")
    if pos>=0:
        return name[pos+1:].lower()
    else:
        return ""
