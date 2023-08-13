#Custom L1 Distance Layer Module
import tensorflow as tf
from tensorflow.keras.layers import Layer

#Custom L1 Distance Layer from Jupyter

class L1Dist(Layer):
    #Init Inheritance
    def __init__(self,**kwargs):
        super().__init__()
        
    #Similarity Calucaltion
    def call(self,input_embedding,validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)