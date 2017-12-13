import logging 
import threading
import time

from PIL import Image, ImageDraw, ImageFont
from picamera import PiCamera

overlay = None
image = None


# cam config 
# HD 720p 
camHeight = 720
camWidth = 1280
camQuality = 23

def camStartRecording(camera):
    logging.info('Starting recording')
    camera.led = True
    camera.start_recording('myVid.h264', format='h264', quality=camQuality)
    return

def camStopRecording(camera):
    logging.info('Stopping recording')
    camera.led = False
    camera.stop_recording()
    return

def camThread(q):
    logging.debug('Starting')
    # initialise
    # start preview 

    global overlay
    global image 
    
    camera = PiCamera()
    camera.resolution = (camWidth, camHeight)
    camera.framerate = 30
    camera.start_preview() 

    text = time.strftime('%H:%M:%S', time.gmtime())
    image = Image.new("RGB", (camWidth, camHeight))
    overlay = camera.add_overlay(image.tostring(), layer=3, alpha=75) 
    draw = ImageDraw.Draw(image)
    draw.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
    draw.text((10, 10), text, (255, 255, 255))
    overlay.update(image.tostring())
    # process q messages
    while True:
        i = q.get()
        logging.debug('get %d' % i)
        q.task_done()
        if i == 'start':
            camStartRecording(camera)
        elif i == 'stop':
            camStopRecording(camera)
        elif i == 5:
            return

    logging.debug('Exiting')   
    return 


def init(q):
    myThread = threading.Thread(name='camThread', target=camThread, args=(q,))
    myThread.start()
    return

