# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from sklearn.neural_network import MLPRegressor
from openram import debug
from openram import OPTS
from .regression_model import regression_model


class neural_network(regression_model):

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

    def get_model(self):
        return MLPRegressor(solver='lbfgs', alpha=1e-5,
                            hidden_layer_sizes=(40, 40, 40, 40), random_state=1)

    def generate_model(self, features, labels):
        """
        Training multilayer model
        """

        flat_labels = np.ravel(labels)
        model = self.get_model()
        model.fit(features, flat_labels)

        return model

    def model_prediction(self, model, features):
        """
        Have the model perform a prediction and unscale the prediction
        as the model is trained with scaled values.
        """

        pred = model.predict(features)
        reshape_pred = np.reshape(pred, (len(pred),1))
        return reshape_pred
