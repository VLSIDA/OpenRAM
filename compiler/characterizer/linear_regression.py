# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from openram import debug
from openram import OPTS
from .regression_model import regression_model


class linear_regression(regression_model):

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

    def get_model(self):
        return Ridge()

    def generate_model(self, features, labels):
        """
        Supervised training of model.
        """

        #model = LinearRegression()
        model = self.get_model()
        model.fit(features, labels)
        return model

    def model_prediction(self, model, features):
        """
        Have the model perform a prediction and unscale the prediction
        as the model is trained with scaled values.
        """

        pred = model.predict(features)
        return pred
