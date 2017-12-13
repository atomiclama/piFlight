import logging 
import threading
import time

def dpThread(q):
    logging.debug('Starting')
    
    for i in range(10):
        time.sleep(0.1)
        q.put(i)
        logging.debug('put %d' % i)
    
    time.sleep(3)
    logging.debug('Exiting')
    
    
def init(q):
    myThread = threading.Thread(name='dpThread', target=dpThread, args=(q,))
    myThread.start()
    return

