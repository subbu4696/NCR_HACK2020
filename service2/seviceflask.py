import tensorflow.keras

import  flask
from flask import jsonify, request, session
import numpy as np
from io import BytesIO
import tensorflow.keras
import Final_queue
from datetime import timedelta
import Constants
#import numpy as np
from PIL import Image, ImageOps
#import cv2
#import json



model = tensorflow.keras.models.load_model('keras_model.h5')
labels = ['low item  cart', 'medium cart', 'full cart', 'random ']
#session['CartWeight']
app = flask.Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(5)
l =[]
D= {'cartsize':None,'Queue':None}


@app.route('/',methods = ['GET'])
def intro():
    print('<h1>Welcome to QueueUp</h1>')


@app.route('/cart',methods = ['POST'])
def getcartsize():
    if request.method == 'POST':

        r = request
        rdata = r.data
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        load_bytes = BytesIO(rdata)
        #load_np = np.load(load_bytes, allow_pickle=True)
        # loaded_np = np.load(data, allow_pickle=True)
        rimg = Image.open(load_bytes, mode='r').convert('RGB')
        size = (224, 224)
        image = ImageOps.fit(rimg, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array
        prediction = model.predict(data)
        #print(prediction)
        #return jsonify(prediction)
        cartsize = labels[prediction.argmax()]
        Queue_Number = None
        if cartsize!='random':
            if cartsize == labels[0]:
                Queue_Number=  Final_queue.queue(Constants.LOW_ITEM_CART)
                l.append(Constants.LOW_ITEM_CART)
            elif cartsize == labels[1]:
                Queue_Number =  Final_queue.queue(Constants.MEDIUM_ITEM_CART)
                l.append(Constants.MEDIUM_ITEM_CART)
            elif cartsize == labels[2]:
                Queue_Number =   Final_queue.queue(Constants.FULL_ITEM_CART)
                l.append(Constants.FULL_ITEM_CART)
            D['cartsize'] =cartsize
            D['Queue'] = Queue_Number+1
            return  jsonify(D)
        else:
            D['cartsize'] = cartsize
            D['Queue'] = 'No Queue'
            return jsonify(D)
    #elif request.method  == 'GET':
            #return jsonify(l)








if  __name__ == '__main__':
    app.run(host='0.0.0.0')
    #print(hello(nam))
    #app.run(debug=True)