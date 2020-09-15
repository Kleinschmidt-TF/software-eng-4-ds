Context
===========

The context module defines context objects used in the Demand Forecast module. A context defines a scope
( i.e which stores, which products) for the model with a specific time windows, or a special mode (e.i backtest).


Two mains contexts are used in the module :

 1. Training Context :

    Scope of the training data.

    .. code-block:: html

        Training context example:

              | -----------INPUT----------- | -----------TARGET------------ |
          2018-12-28----------8----------2019-02-21----------6----------2019-04-04

        Store ID : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Number of product : 100



 2. Prediction Context  :

    Scope of the prediction data. It includes the backtesting context if `backtest` is enabled.

    .. code-block:: html

        Prediction Context :

            | -----------INPUT----------- | -----------TARGET----------- |
        2019-04-05----------8----------2019-05-30----------6----------2019-07-11

        Store ID : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Number of product : 100


Meta Context
~~~~~~~~~~~~~~~~~~

.. automodule:: src.context.meta
    :members:

Training Context
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.context.training_context
    :members:

Prediction Context
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.context.prediction_context
    :members: