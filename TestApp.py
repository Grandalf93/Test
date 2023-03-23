# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:18:28 2023

@author: juand
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 12:38:35 2023

@author: juand
"""

from flask import Flask, render_template, request, jsonify, Response
import RPi.GPIO as GPIO
from mpyg321.MPyg123Player import MPyg123Player
from CameraCV import VideoCamera
from gtts import gTTS
import logging
import cv2



#sys.path.append('../')
app = Flask(__name__, template_folder="templates")
video_camera = VideoCamera()
player = MPyg123Player()

#set speed




#GPIO Setup
GPIO.setmode(GPIO.BOARD)

#Motor D
GPIO.setup(7, GPIO.OUT)#IN A-D
GPIO.setup(11, GPIO.OUT)#EN A-D
GPIO.setup(12, GPIO.OUT) #PWM motor D
GPIO.setup(13, GPIO.OUT)#IN B-D

p = GPIO.PWM(12, 50)
p.start(50)

GPIO.output(7, False)
GPIO.output(11,False)
GPIO.output(13, False)

#Motor I
GPIO.setup(16,GPIO.OUT)#IN A-I
GPIO.setup(18,GPIO.OUT)#EN A-I 
GPIO.setup(19,GPIO.OUT) #PWM motor I
GPIO.setup(21,GPIO.OUT)#IN B-I

pI = GPIO.PWM(19, 50)
pI.start(50)

GPIO.output(16, False)
GPIO.output(18,False)
GPIO.output(21, False)



@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/message')
def tts():
    mensaje_tts = request.args.get('val')
    tts = gTTS(mensaje_tts, lang='es')
    tts.save('test.mp3')
    
    player.play_song('test.mp3')
    app.logger.info("mensaje recibido: %s ", mensaje_tts)
 
    data = {
        "Mensaje": mensaje_tts           
        }
    

    return jsonify(data)

@app.route('/cell_interface')
def cellphone_index():
    return render_template('cellphone_index.html')

@app.route('/stream_video')
def stream_video():
    return Response(gen(video_camera),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/motor')
def  motor_control():
    direction = request.args.get('var')
    value = request.args.get('val')
    
    
    if direction == "speed":
        speed = float(value)
        p.ChangeDutyCycle(speed)
        pI.ChangeDutyCycle(speed)
        print("LOG1")
    else:
        pass

        

    
    
    if (value=="1"):       
        if(direction == "up_button"):
            GPIO.output(7, False)
            GPIO.output(11,True) #EN
            GPIO.output(13, True)

            GPIO.output(16, False)
            GPIO.output(18, True) #EN
            GPIO.output(21,True)        
            
        

        if(direction == "down_button"):
            GPIO.output(7, True)
            GPIO.output(11,True) #ENABLE
            GPIO.output(13, False)

            GPIO.output(16, True)
            GPIO.output(18, True) #ENABLE
            GPIO.output(21,False)

        if(direction == "right_button"):
            GPIO.output(7, True)
            GPIO.output(11,True) #ENABLE
            GPIO.output(13, False)

            GPIO.output(16, False)
            GPIO.output(18, True) #EN
            GPIO.output(21,True)   

        if (direction == "left_button"):

            GPIO.output(7, False)
            GPIO.output(11,True) #EN
            GPIO.output(13, True)

            GPIO.output(16, True)
            GPIO.output(18, True) #ENABLE
            GPIO.output(21,False) 
    else:       
            
        GPIO.output(7, False)
        GPIO.output(11,True)
        GPIO.output(13, False)

        GPIO.output(16, False)
        GPIO.output(18, True)
        GPIO.output(21 ,False)    

            
            
                
    
            
    
    data = {
        "Direccion": direction,
        "Movimiento":value        
        }
    
    return jsonify(data)   
    
    



if __name__ == "__main__":
    app.run(host="0.0.0.0")