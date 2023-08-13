from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
import cv2
import tensorflow as tf
from layers import L1Dist
import os
import numpy as np

class CamApp(App):
    
    def build(self):
        #Visulization layout
        self.web_cam = Image(size_hint=(1,.8))
        self.button = Button(text="Verify", on_press=self.verify ,size_hint=(1,.1))
        self.verification_label = Label(text="Verification Uninitiated", size_hint=(1,.1))
       
        #Adding the paramaters to layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification_label)
        
        #Load model
        self.model = tf.keras.models.load_model('siamesemodel.h5',custom_objects={'L1Dist':L1Dist})
        
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update,1.0/33.0)

        return layout
  
    def update(self,*args):
        #Taking frames from capture, and resizing it to only capture head
        ret, frame = self.capture.read()
        frame = frame[120:120+250,200:200+250, :]
        #Flipping Image and converting it a useable img form for kivy
        buf = cv2.flip(frame,0).tostring()
        img_texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        img_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
        self.web_cam.texture = img_texture
        
    def preprocess(self,file_path):
        #Reading in image from file path
        byte_img = tf.io.read_file(file_path)
        #Load in Image
        img = tf.io.decode_jpeg(byte_img)
        #Preprocess(Reize image to 100x100x3)
        img = tf.image.resize(img,(100,100))
        #Scaling the image to be between 0 and 1
        img = img/255.0
        return img
    def verify(self,model):
        #Thresholds
        detection_threshold = 0.5
        verification_threshold = 0.5
        
        #Capture input image
        SAVE_PATH = os.path.join('application_data','input_image','input_image.jpg')
        ret, frame = self.capture.read()
        frame = frame[120:120+250,200:200+250, :]
        cv2.imwrite(SAVE_PATH,frame)
        results = []
        
        for image in os.listdir(os.path.join('application_data','verification_images')):
            input_img = self.preprocess(os.path.join('application_data','input_image','input_image.jpg'))
            validation_img = self.preprocess(os.path.join('application_data','verification_images',image))
            
            result = self.model.predict(list(np.expand_dims([input_img,validation_img],axis=1)))
            results.append(result)
        detection = np.sum(np.array(results)>detection_threshold)
        verification = detection / len(os.listdir(os.path.join('application_data','verification_images')))
        verified = verification > verification_threshold
        
        #Set verification label
        self.verification_label.text = 'Verified' if verified == True else 'Unverified'
    
        
        return results, verified
    
if __name__ == '__main__':
    CamApp().run()