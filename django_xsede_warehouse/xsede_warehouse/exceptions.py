import logging
logg2 = logging.getLogger('xsede.glue2')

class ProcessingException(Exception):
    def __init__(self, response, status):
        self.response = response
        self.status = status
        logg2.error('%s status=%s (%s)' % (type(self).__name__, repr(self.status), repr(self.response)))
    def __str__(self):
        return repr(self.status)
