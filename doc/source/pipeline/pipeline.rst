Task
===========

Description
~~~~~~~~~~~~~~~~~~~~~~~~

The Task module handles the pipeline of the run and manages all the different steps.

This module consists of :
 - ``stages`` submodule that defines the ``Stage`` object. Stages are defined sequentially and are specific to the demand forecast use case.
   One Stage corresponds to a specific step of the pipeline. This object is instantiated with a name like ``"TRAINING_FETCH"``
   and contains comparison methods like ``__eq__``, ``__gt__``, ... to use the following operator on the ``Stage`` object :
   ``stage_a < stage_b``

 - ``operators`` submodule that defines the ``Òperator`` object. An operator is a step in a pipeline, that executes a task,
   given a configuration, a stage and data, and updates the stage. Operators have dependencies (on other operators / on the stage).
   An operator  is defined with an ``operator_id``, a ``final_stage`` and a function ``python_callable``

 - ``pipeline`` submodule that defines the ``Pipeline`` object. A ``Pipeline`` is a set of tasks (``Operator``) organized with dependencies.
   Running a Pipeline will execute the Operators according to their dependencies.
   Here, dependencies are linear and linked to ``Stages``: the Pipeline starts from a ``begin_stage``,
   then executes each ``Operator`` and moves to the next stage and ends to a ``final_stage``.
   A Pipeline run in test mode will trigger a check of the Operator's output against a reference Scenario.

 - ``demand_forecast`` submodule that defines the ``DemandForecastPipeline``. This module defines first all the methods that
   will be run sequentially. And from a method and a final_stage, an operator is defined.
   The ``DemandForecastPipeline`` inherits from the ``Pipeline`` class and is instantiated with the list of Operators defined at
   the beginning of this submodule.

How to use it
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    from src.services.service_provider import ServiceProviderHandler
    from src.tasks.operators import Operator
    from src.tasks.pipeline import Pipeline
    from src.tasks.stages import DFStages, Stage

    # Define method to run in the pipeline
    def method_a():
        print("Start")

    # Define the corresponding stage
    stage_a = Stage("INIT")

    # Define the corresponding operator
    operator_a = Operator(
        operator_id="operator_a",
        final_stage= stage_a,
        python_callable=method_a
    )

    # Define another method
    def method_b():
        print("Ends")

    stage_b = Stage("END")

    operator_b = Operator(
        operator_id="operator_b",
        final_stage= stage_b,
        python_callable=method_b
    )

    # Create the operator list, basis of the pipeline
    operators_  = [ operator_a, operator_b]

    # Instantiate the pipeline
    myPipeline = Pipeline(
        begin_stage=stage_a,
        final_stage= stage_b,
        operators=operators_,
        test=False
    )

    # Run the pipeline
    myPipeline.run()


Pipeline Base Class
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.tasks.pipeline
    :members:


Demand Forecast Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.tasks.demand_forecast
    :members:

Operators Base Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.tasks.operators
    :members:

Stages Base Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.tasks.stages

    :members:
