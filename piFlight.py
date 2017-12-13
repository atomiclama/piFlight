#!/usr/bin/env python

from Queue import Queue
import logging

import piCam 
import piDisplayPort 
import piIO 


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
    logging.debug('Starting')
    
    # create queue for communicating between threads.
    cam_q = Queue()
    piCam.init(cam_q)
    piDisplayPort.init(cam_q)
    piIO.init(cam_q)
        
    # Main thread work is done 
    logging.debug('Exiting')
    pass
