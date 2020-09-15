"""
This script contains machine learning models factory for demand forecast module
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

from src.backtest.utils import calculate_bias, calculate_smape
from src.services.service_provider import ServiceProviderHandler
from .models.model import MetaModel

SERVICE = ServiceProviderHandler()


class DemandMLModel:
    """
    Class allowing to train and predict demand with a machine learning model
    """

    def __init__(self, name: str, params: dict):
        super().__init__()

        # Input
        self.name = name
        self.params = params

        # instantiate the model
        try:
            self.model = getattr(MetaModel, self.name)(**self.params)
        except KeyError:
            raise ValueError(f"model_name {self.name} is not yet supported")

        # Cross-validation
        self.use_cross_val = bool(
            SERVICE.config.run_param.use_cross_validation
        )
        self.nb_folds = int(SERVICE.config.run_param.nb_folds) \
            if self.use_cross_val else None

        self.columns = None  # column used when training the model
        self.is_fitted = False  # to check if model is fitted

    def fit(self, x_train: pd.DataFrame, target: pd.Series):
        """
        Train machine learning model
        """
        SERVICE.log.info(f"Training of model {self.name}")

        features = x_train.copy()
        self.columns = list(features.columns)

        if self.use_cross_val:
            self.cross_validate(features, target)

        # Training model
        SERVICE.log.info(f"Training set shape is {features.shape}")
        self.model.fit(features, target)
        self.is_fitted = True
        SERVICE.log.info("Model fitted")

        return self.model

    def predict(self, x_pred: pd.DataFrame):
        """
        Predict with trained machine learning model
        """
        SERVICE.log.info(f"Predicting with trained model {self.name}...")
        assert set(x_pred.columns) == set(self.columns), \
            set(x_pred.columns).symmetric_difference(set(self.columns))
        x_pred = x_pred[self.columns]
        predictions = self.model.predict(x_pred)
        return predictions

    def cross_validate(self, features: pd.DataFrame,
                       y_train: pd.Series) -> None:
        """
        Perform cross validation
        """
        SERVICE.log.info(
            f"Performing cross validation on {self.nb_folds} folds...")
        kf = KFold(n_splits=self.nb_folds)

        x_data, target = features.copy(), y_train.copy()

        # Train and predict in each fold to compute metrics
        biases, smapes = [], []
        for i, (train_index, test_index) in enumerate(kf.split(x_data)):
            # Define subset to train and predict with
            x_train = x_data.loc[x_data.index.isin(train_index)]
            y_train = target.loc[target.index.isin(train_index)]
            x_test = x_data.loc[x_data.index.isin(test_index)]
            y_test = target.loc[target.index.isin(test_index)]

            SERVICE.log.info(
                f"{i + 1} : train shape is {x_train.shape[0]}, "
                f"test shape is {x_test.shape[0]}"
            )

            # Fit and predict
            self.model.fit(x_train, y_train)
            predictions = self.model.predict(x_test)

            # Evaluate
            biases.append(calculate_bias(predictions, y_test))
            smapes.append(calculate_smape(predictions, y_test))

        train_metrics = (np.mean(biases), np.mean(smapes))
        SERVICE.log.info(f"Cross-validation metrics : {train_metrics}")

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
