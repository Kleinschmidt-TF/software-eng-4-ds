Demand Forecast
=====================

The demand_forecast module handles the ML model and the final data processing module.

1. The ``model`` submodule includes all the predefined or custom-made ML model. A model factory allows
to easily change and test different model only based on a model name (in the config). This factory is defined in the
``MetaModel`` object with a ``fit`` and a ``predict`` method.

2. The ``params`` submodule contains all parameters necessary for the training model.

3. The ``processing`` submodule contains all methods necessary for the feature engineering.
It contains as well the DataPipeline object that handle the sequence of feature engineering steps

Demand Forecast Module
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.demand_forecast.demand_forecast
    :members:

Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.demand_forecast.params.module_params
    :members:

Feature Engineering
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.demand_forecast.processing.feature_engineering
    :members:

.. automodule:: src.demand_forecast.processing.data_pipeline
    :members:


Machine Learning models
~~~~~~~~~~~~~~~~~~~~~~~~

Demand ML model
##########################
.. automodule:: src.demand_forecast.ml_model.demand_ml_model
    :members:

Tree based model
##########################
.. automodule:: src.demand_forecast.ml_model.models.model
    :members:
