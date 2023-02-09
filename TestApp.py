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
from mpyg321.MPyg123Player import MPyg123Player
from CameraCV import VideoCamera
from gtts import gTTS
import logging
import cv2



#sys.path.append('../')
app = Flask(__name__, template_folder="templates")
video_camera = VideoCamera()
player = MPyg123Player()


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

@app.route('/stream_video')
def stream_video():
    return Response(gen(video_camera),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/motor')
def  motor_control():
    direction = request.args.get('var')
    value = request.args.get('val') 
    data = {
        "Direccion": direction,
        "Movimiento":value        
        }
    
    return jsonify(data)
    
    
    



if __name__ == "__main__":
    app.run(host="0.0.0.0")