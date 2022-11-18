
import glob
import logging

from datetime import datetime
from rich.logging import RichHandler
from elasticsearch import Elasticsearch, helpers 

logging.basicConfig( level = 'NOTSET', format = '%(message)s', datefmt = '[%X]', handlers = [RichHandler()] )
log = logging.getLogger('rich')

class Elastic:
    def __init__(self, host, dictionary, file_type) -> None:
        try: self.host  = Elasticsearch(host)
        except ValueError: 
            log.error('Host must be a URL example: https://localhost:9200')
            exit()
        self.files = list(glob.iglob('%s/*.%s' % (dictionary, file_type), recursive=True))

    def start(self):
        for file in self.files:
            action = list()
            file_name = file.split('\\')[-1]

            try:
                for line in open(file = file, mode = 'r', encoding = 'cp1252', errors = 'replace').readlines():
                    line = ' '.join(line.rstrip().split())
                    try:
                        data = {
                            '_index': 'logs',
                            '_source': {
                                'title': file_name,
                                'data': line,
                                'added': datetime.now()
                            }
                        }

                        action.append(data)
                    except Exception as e:
                        log.error('Error: %s' % e)
                        return
                        
            except Exception as e:
                log.error('Error: %s' % e)
                return

            try:
                log.info('Importing %s records from %s!' % (len(action), file_name))

                helpers.bulk(
                    self.host.options(request_timeout=800000000000000, retry_on_timeout = False), 
                    actions = action,
                    refresh = True,
                )

                log.info('Added %s to cluster from %s!' % (len(action), file_name))
            except Exception as e:
                log.error('Error: %s' % e)

log.info('Starting Import!')

EsImport = Elastic(
    host       = 'http://localhost:9200',
    file_type  = 'csv',
    dictionary = './data'
)

EsImport.start()
