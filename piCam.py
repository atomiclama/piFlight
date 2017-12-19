import logging 
import threading
import time

from PIL import Image, ImageDraw, ImageFont
from picamera import PiCamera

overlay = None
image = None


# cam config 
# HD 720p 
camHeight=720
camWidth=1280


#mode 5 16:9
# camHeight=730
# camWidth=1296

#  mode 4 4:3
# camHeight = 972
# camWidth = 1296


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
    camera.framerate = 49
    camera.rotation = 180
    camera.start_preview(anamorphic=True)
    
#     camera.start_preview(resolution=(720,576)) 
   
    
    text = time.strftime('%H:%M:%S', time.gmtime())
    image = Image.new("RGBA", (camWidth, camHeight))
    overlay = camera.add_overlay(image.tobytes(), layer=3, format='rgba', size=(camWidth, camHeight), anamorphic=True) 
    draw = ImageDraw.Draw(image)
    draw.font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 50)
#     draw.text((10, 10), text, (255, 255, 255))
#     draw.text((45,10), "123456789", (255, 255, 255))
#     overlay.update(image.tobytes())
    # process q messages

    while True:
        i = q.get()
       
        q.task_done()
        draw.rectangle([0,0,300,100],fill=(255, 255, 255, 0))
#         draw.text((45,10), text, fill=(255, 255, 255, 0))
        text = time.strftime('%H:%M:%S', time.gmtime())

        draw.text((45,10), text, fill=(255, 255, 255, 128))
        overlay.update(image.tobytes())
#         camera.preview.rotation = camera.preview.rotation + 180
#         global camHeight
#         camHeight = camHeight +16
#         camera.resolution = (camWidth, camHeight)
        logging.debug('width height %d:%d', camWidth, camHeight)
#         logging.debug('anamorphic %d ', camera.preview.anamorphic)
        
        if i == 'start':
            camStartRecording(camera)
        elif i == 'stop':
            camStopRecording(camera)
        elif i == 'exit':
#             continue
            break
        else:
            logging.debug('get %d' % i)

    logging.debug('Exiting')   
    return 


def init(q):
    myThread = threading.Thread(name='camThread', target=camThread, args=(q,))
    myThread.start()
    return

