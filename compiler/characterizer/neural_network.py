# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from .regression_model import regression_model
from globals import OPTS
import debug

from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf


class neural_network(regression_model):

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

    def generate_model(self, features, labels):
        """
        Supervised training of model.
        """
        
        model = keras.Sequential([
            layers.Dense(32, activation=tf.nn.relu, input_shape=[features.shape[1]]),
            layers.Dense(32, activation=tf.nn.relu),
            layers.Dense(32, activation=tf.nn.relu),
            layers.Dense(1)
        ])

        optimizer = keras.optimizers.RMSprop(0.0099)
        model.compile(loss='mean_squared_error', optimizer=optimizer)
        model.fit(features, labels, epochs=100, verbose=0)
        return model
        
    def model_prediction(self, model, features):    
        """
        Have the model perform a prediction and unscale the prediction
        as the model is trained with scaled values.
        """
        
        pred = model.predict(features)
        return pred
        