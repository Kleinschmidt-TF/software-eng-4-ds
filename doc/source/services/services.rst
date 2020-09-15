Services
=============

Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Service is the module that allows to handle the log, the database, the config and the filesystem.
The goal of this script is to make these 4 services unique even if one of these classes will be instantiated several times.
The Singleton method allows to keep the service unique along the `Demand Forecast` module.


How to use it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    from src.services.service_provider import ServiceProviderHandler

    SERVICES = ServiceProviderHandler()

    class Foo:

        def __init__(self):

            self.bar = SERVICES.config.name
            SERVICES.log.info('New class instanciated')


Services Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.services.service_provider
    :members:

Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.services.config.config_handler
    :members:

Data Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.services.db.db_handler
    :members:

Filesystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FileSystemHandler
################################
.. automodule:: src.services.filesystem.filesystem_handler
    :members:

Scenario
################################

Description
********************************

The ``Scenario`` object is a simple data versioning system of your runs and allows to manage your different scenarios by saving
the corresponding data and config. It is based on a directory where the config, the run information  and the output data are stored.
The scenario object has these following properties :
    - ``name``
    - ``locations``
    - ``hash``
    - ``dtcreated``
    - ``stage``
    - ``git_hash``
    - ``config``

This Scenario object allows as well to make the output replicable.

This class allows to load directly a scenario and compare two different scenarios on :
config, code, data, model, score,...

How to use it
********************************

.. code-block:: python
    :linenos:

    from src.services.filesystem.scenario import Scenario
    from src.services.config.config_handler import Config

    config = Config("./config/model_config.yml")

    # Instantiate a new scenario
    new_scenario = Scenario(
            input_path="./tmp",
            config=config
    )

    # Load an existing scenario
    loaded_scenario = Scenario.load(
            scenario_path="./tmp/demand_prediction_1"
    )

    # Compare two scenarios
    check = new_scenario.compare(loaded_scenario)


.. automodule:: src.services.filesystem.scenario
    :members:

Read service
################################
.. automodule:: src.services.filesystem.read_service
    :members:

Write service
################################
.. automodule:: src.services.filesystem.write_service
    :members: