import random
import matplotlib.pyplot as plt

import pickle
import itertools
import numpy as np
import tensorflow.keras as keras
import pandas

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Lambda

with open('../data/HackathonMetadata.pkl','rb') as ff: 
    metad = pickle.load(ff) 

with open('../data/HackathonData_Homology0.pkl','rb') as ff: 
    homol = pickle.load(ff)

def pairs_generator(batch_size = 1024):
    bl1, bl2 = [], []        
    while True: 
        
        i = np.arange(homol['indata'].shape[0])
        random.shuffle(i)
        j = np.arange(homol['indata'].shape[0])
        random.shuffle(j)
        
        for e, k in enumerate(zip(i,j)):
            if k[0] != k[1]:
                bl1.append(k[0])
                bl2.append(k[1])
                if len(bl2) == batch_size:
                    yield [homol['indata'][bl1], homol['indata'][bl2]], homol['distdata'][bl1,bl2]
                    bl1 = []
                    bl2 = []

def singleton_generator(batch_size = 1024):
    iterator = range(homol['indata'].shape[0])
    for e, i in enumerate(iterator):
        yield homol['indata'][i][None,:]                        

input_shape = homol['indata'].shape[1]

left_input = layers.Input(input_shape)
right_input = layers.Input(input_shape)
model = keras.Sequential()
model.add(layers.Dense(128, activation='relu', 
                       kernel_initializer=keras.initializers.RandomUniform(minval=-2, maxval=2), 
                       bias_initializer=keras.initializers.RandomUniform(minval=0, maxval=0.5), ))

model.add(layers.Dropout(0.2))
model.add(layers.Dense(2, activation='linear', 
                       kernel_initializer=keras.initializers.RandomUniform(minval=-2, maxval=2), 
                       bias_initializer=keras.initializers.RandomUniform(minval=0, maxval=0.5), ))
encoded_l = model(left_input)
encoded_r = model(right_input)
dist_output = layers.Dot(axes=1)([encoded_l, encoded_r])
siamese_net = keras.Model(inputs=[left_input,right_input], outputs=dist_output)

optimizer = keras.optimizers.Adam(lr = 0.00006)
siamese_net.compile(loss="binary_crossentropy",optimizer=optimizer)

epochs = 100
siamese_net.fit(pairs_generator(), steps_per_epoch=1000, epochs= epochs)

memb = keras.Model(inputs=[left_input], outputs=encoded_l)
embed = memb.predict(singleton_generator())
