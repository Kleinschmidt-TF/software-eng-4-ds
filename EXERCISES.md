# Exercises

Make sure you have follow the [README](./README.md) instructions before starting the exercises.

## Setup a virtual environment 

In order to complete the use case 1, you have to setup a virtual environment on your machine. To do so please :
- Checkout on branch `training/ex-basics` 
- Create a virtual environment (e.g `python -m venv venv`)
- Activate your environment (e.g `source venv/bin/activate`)
- Install requirements
    - `pip install --upgrade pip`
    - `pip install -r requirements.txt`
    
(As a reminder you can access a jupyter notebook within your virtual environment by running `venv/bin/jupyter notebook` at the root of your repo)


## Exercise 1.1 - Notebook beginning - (branch : origin/training/ex-basics)

You are a Data Scientist who worked for 3 weeks on a demand forecast prediction case for an international retailer.
You have a first version of your model in the notebook located here: `./original_work.ipynb`.
Now you need to industrialize your code and move your model in a proper script.

Take 5-10' to look at the notebook and think about the possible issues with a Nb approach and try to provide a first solution to address it.

Do not focus on the accuracy of the model, but rather on what a good code structure should look like.

## Exercise 1.2 - Organize your code - (branch : origin/training/ex-class-df)

### Context

A first step could be moving your code from the notebook to a structured Python script.
A good approach is to use the OOP to organize your code. 
The units (i.e. objects, methods) all have a unique specific purpose by design (data loader, pre-processing, model training, etc.)


### Task

1. From the `original_work.ipynb`, organize a structured script with a main class and several methods.
To do so, in `local_model.py` in the root of the repo, build a `DemandForecast` class instantiated with a config dictionary and containing these following methods:
  - __init__()

  	Instantiate the DemandForecast class
  	- args : config (dict)
  	- return : self

  - load()

  	Load the 3 files from an input directory and set it as attributes
  	- args : input_path  (str)
  	- return : None

  - preprocess()

  	Preprocess data to return one dataframe
  	- args: None
  	- return : pd.DataFrame

  - process()

  	Process the dataframe to process features and split it to return X_train, X_test, y_train , y_test
  	- args : data = pd.DataFrame
  	- returns : (pd.DataFrame, pd.DataFrame, pd.Series, pd.Series)

  - fit()

    Train your algorithm on a training set
  	- args : X_train , y_train (pd.DataFrame, pd.Series)
  	- return : None

  - predict()

  	Predict on a test set
  	- args : X_test (pd.DataFrame)
  	- return : pd.Series

  - evaluate()

  	Evaluate your score with a given metrics
  	- args : y_test, y_pred (pd.Series, pd.Series)
  	- return : float


### How to

1. Create `local_model.py` in the root directory and code here.
2. Test your code with `pytest test_exercise.py`.

### Detailed instructions

You can use `setattr` to set an attribute in a class. The input configuration dictionary is flat (simpler than the one in `model_config.yml`), i.e.
```python
config = {"n_estimators": ..., "random_state": ..., }
```

## Exercise 1.3 - End-to-end test - (branch : origin/training/ex-e2e)

### Context

Now that you have moved your code in .py script, you need to make sure that the results are unchanged for a given config.

An end2end test will ensure refactoring the code do not affect our results.
### Task

1. Create a `test_end_to_end` test method in your `DemandForecast` class to compare prediction of your model with a given test folder containing a config and a prediction.
It should return an `assert` error if the output is different otherwise it returns `True`. The `test_end_to_end` method should take a test folder as argument.
Your test should use the `config.yml` and the `predictions_test.csv` from the existing `tests` folder to compare your predictions.

2. Create a basic versioning system with the method `save` that allows to save in a unique folder : 
	- your config in a yaml file `config.yml`, 
	- the hash of the current commit, the name of the scenario and the datetime of creation in a yaml file `info.yml` with (```key = "name"```)
	- the predictions in a csv format called `predictions.csv`

	The output folder and the folder name  (name of the scenario) will be passed as argument.

Example of utilisation :
```python
demandforecast.save(output_path = pl.Path('./tmp'),  name = 'scenario_1')
```

### How to

1. Code the method in `local_model.py`.
2. Test your code with `pytest test_exercise.py`.

### Detailed instructions

* Use the following command to get the current hash commit :
```python
import git
repo = git.Repo(search_parent_directories=True)
hash_git = repo.head.object.hexsha
```

* Use the following command to save yaml files:
```python
import yaml
with open(config_path, "w") as _file:
    yaml.safe_dump(self.config, _file, default_flow_style=False)

```

## Part 2:

## Exercise 2.1 - Demand Forecast Module - (branch : origin/training/ex-sol-p1)

Congratulation, you have a first structured version of your code with some tests implemented. You can
 find a solution in `model.py`. However, this is not sufficient to make this module
flexible, robust, reproducible and easily deployable.

Take 5-10' to think about a relevant architecture for this forecast code, you can make group of 2-3 persons. We will align all together on the target architecture.
The target structure should cope with all the issues you raised in the discussion.

## Exercise 2.2 - Config class - (branch : origin/training/ex-read-only-config) :

### Context

A first step to make your code more robust is to ensure that your configuration can not be changed once initialized during a run.
To do so, you will make it immutable.

### Task

1. You need to define a Config class which inherits from a `collections.Mapping` class. This method allows to make the config
immutable and none of the config parameters can be changed in the codebase, i.e `config['db']= "database"` is not allowed.
You need as well to implement abstract methods from `collections.Mapping`

    `Config` is initialized with a yaml path.
    
    ```python
    config = Config(pl.Path("configs" / "model_config.yaml"))
    ```
    
    Your dictionary needs to be wrapped in a `Box` class from the box package with `frozen_box=True` to make the attribute immutable.
    See [here](https://pypi.org/project/python-box/).

2. You need to add a `is_config_valid` method called in the `__init__` to check if your file fits with
a predefined Schema from the the `schema` module. In `src.services.config.config_schema` you need to create the
schema for the `infra_config.yaml` file.

3. Add this part of code in your class to not allow `__setattr__` ( i.e `config.db = "database"` is not allowed) and is let immutable.

    ````python
        def __getattr__(self, item):
            return self.__data[item]

        def __setattr__(self, key, value):
            """Here if the attribute `_initialized` has been set to True,
            It is not possible to set anything to an (existing) attribute"""
            if self.__dict__.get('_initialized'):
                raise Exception("Attribute is Read-Only")
            super().__setattr__(key, value)

        def to_dict(self):
            return self.__data.to_dict()

        def __delattr__(self, item):
            raise Exception('Cannot delete attribute')
    ````

4. Similarly, add this part in the `__init__`:

    ````python
     self._initialized = True
    ````
`_initialized` is set to True in the `__init__`, then,
it is not possible to set anything to an (existing) attribute.

### How to
1. Create a `local_config_handler.py` in `src/services/config` and code here.
2. Test your code with `pytest test_exercise.py`.

### Detailed instructions

1. `collections.Mapping` is an abstract class, that's why you need to add the specific abstract methods. 
For example, since `__len__` is an abstract method required from `collections.Mapping`, your derived class needs
the following method implemented:
    ```python
    def __len__(self):
        return len(self.__data)
    ```
    You can look at [here](https://docs.python.org/3.4/library/collections.abc.html)
    the required abstract methods of `collections.Mapping`.

2. Find below a basic example of schema validation process:
```python
>>> from schema import Schema, And, Use, Optional

>>> schema = Schema([{'name': And(str, len),
...                   'age':  And(Use(int), lambda n: 18 <= n <= 99),
...                   Optional('gender'): And(str, Use(str.lower),
...                                           lambda s: s in ('squid', 'kid'))}])

>>> data = [{'name': 'Sue', 'age': '28', 'gender': 'Squid'},
...         {'name': 'Sam', 'age': '42'},
...         {'name': 'Sacha', 'age': '20', 'gender': 'KID'}]

# Validate the `data` dictionary through the schema `schema`
>>> validated = schema.validate(data)
```

`Schema` can have `Optional` keys. Value can have a `Or` statement

For instance :
```python
Optional('products'): Or(list, None)
```
*Inheriting from the`collections.Mapping` class prevents from setting an item that is already set. However, a dictionary attribute remains mutable 
(i.e. you can update the values without changing the underlying id). Using `Box` with `frozen=True` disables that mutability too. 
The combined solution ensures that your config object cannot be altered once the instance is initialized (hence your whole run always uses the same 
configuration parameters)*

### Solution

* Solution: available in next exercise

## Exercise 2.3 - Configuration Handler - (branch : origin/training/ex-config-handler) :

### Context

To continue the work done in 2.2 to robustify the code, you will now implement a singleton to ensure the configuration unicity.
It will guarantee that every time you instantiate the configuration, the same object will be returned (and not a new one).

### Task
You need to define a singleton class `ConfigHandler` that will hold the whole configuration, gathered from the `.yaml` files in `configs` directory.

`ConfigHandler` is called in multiple places of the code but should be a singleton. This means that all instances are actually the same:

```python
config = ConfigHandler(yaml_directory=CONFIG_PATH)  # creates the ConfigHandler instance (singleton)
config_bis = ConfigHandler(yaml_directory=CONFIG_PATH)  # returns the same object than config
config_ter = ConfigHandler() # returns the same object than config
```

ConfigHandler should have one attribute per file. The attribute name should be the file base name and the values should be a `Config` instance.

### How to
1.  Code in `local_config_handler.py` in `src/services/config`.
2. Test your code with `pytest test_exercise.py`

### Detailed instructions
1. Define the singleton class `ConfigHandler`. This class uses the `__new__` method to make it unique.
2. `ConfigHandler` needs to have as attributes, all config files name equals to an instance of the `Config` class.
It needs to be a proxy to access the configuration defined in `configuration/*.yaml` files.
See the example below:

```python
config = ConfigHandler(yaml_directory=CONFIG_PATH)  # returns the ConfigHandler
infra_config = config.infra_config  # Config of infra configuration as defined in configuration/infra_config.yaml
model_config = config.model_config  # Config of model configuration as defined in configuration/model_config.yaml
model_config.run_info.run_mode  # returns the value stored under run_info > run_mode in configuration/model_config.yaml
```
To add a `Config` object as a class attribute of ConfigHandler with the name `config_a`, you can do in the
specific ConfigHandler method:
````python
setattr(
    cls,
    'config_a',
    Config(yaml_directory / 'config_a.yaml'),
)

# allow to call `config_handler.config_a` (equal to Config(yaml_directory / 'config_a.yaml))
````


### Solution

* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-config-solution/src/services/config/local_config_handler.py)
* Full implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/services/config/config_handler.py)

## Setup your docker environment

### UC2 using Docker (Option 1)
In order to complete the use case 2, you can setup a docker environment as described in the README.

To make sure the interpreter is well configured you can run `pytest` on `test/` folder in `training-se` branch. Every tests should pass.

In order to complete the following exercises, you have to checkout on the branch, modify the code and test it with `test_exercise.py` script. 
To do so you can __either__:
- Use your IDE : run `pytest` directly on the script with [here](https://www.jetbrains.com/help/pycharm/creating-and-editing-run-debug-configurations.html).
  The new configuration will be `python tests`, the script path is `test_exercise.py` and the interpreter is the docker-compose interpreter. 
- Use the command line : run `docker container run -it -v $(pwd):/code --network training-se_local training-se_model bash` and use `pytest` like in a normal shell

### UC2 using Conda/VENV

If you don't want to use docker to run the model and your tests, you can update
your environment by doing:
```
pip install -r requirements.txt
```
in your environment.

And following these next steps:

In order to complete the following exercises, you have to checkout on the branch, modify the code and test it with `test_exercise.py` script. 
To do so you can __either__:
- Use your IDE : run `pytest` directly on the script with [here](https://www.jetbrains.com/help/pycharm/creating-and-editing-run-debug-configurations.html).
  The new configuration will be `python tests`, the script path is `test_exercise.py` and the interpreter is your conda/venv interpreter. 
- Use the command line : run  `pytest text_exercise.py` 


## Exercise 2.4 - OOP - (branch : origin/training/ex-oop)

Before starting the exercise 2.4, please take a time to have a look at Repo structure [here](https://github.gamma.bcg.com/pages/swe-training/training-se/project_structure/structure.html#structure-of-demand-forecast-module).

### Context

As a Data scientist, you are likely to run multiple scenarios and especially, you might be asked to reproduce results a while after running a scenario.
In order to deal with this more easily, you will build a scenario class to keep your runs organized.

The `scenario` class is a Python object based on a scenario directory that contains your input/output data and configuration of your run. It allows to have
a robust data structure with a basic versioning file system.
This scenario allows the user to keep his/her run with a unique ID, its config, its input and its output data.
Then the class scenario would be able to compare two scenarios, and check if the code, the config, the output or the data are different.

A scenario has also a `stage` property referring to the current pipeline stage of the scenario. It means that the run can be stopped to a given stage.
The scenario will have a `load` class method in order to read a scenario from a given path. This allows as well to run the model from the current scenario stage.

### Task

1.  You need to work in `src/services/filesystem/local_scenario.py`

2. Implement the following properties in a `Scenario` class that inherit from `ScenarioMeta`:
	- name : name of the scenario
	- stage : initial stage of the scenario (with a setter method)
	- location : path of the scenario (input_path / name)
	- hash : hash based on the config and the git hash. (git_hash from MetaScenario with `self.git_hash`)
	- config : config of the current scenario (Config class)

    This class will be initialized with the properties above. Each property has a `@property` method to get the value. Only `stage` and `test` has a setter method.
    `ScenarioMeta` is implement in `src/services/filesystem/scenario.py`

 4. Use `self.CONFIG` and `self.INFO` (from Container) to get the names of the backups of the config and info `.yaml` files.

    Example of utilization:

    ```python
    scenario = Scenario(input_path="/tmp", config=scenario_test.config, name="scenario_1")
    ```

5. Build a `classmethod` called `load` that allows to load a scenario from a `scenario_path`.

    Example of utilization:
    ```python
    scenario_test = Scenario.load(scenario_path=pathlib.Path("test") / "data_test" / "demand_prediction")
    ```

    Here you need to read the `info.yaml` from the scenario (`scenario_path`) to update each attribute (`_info`,`_name`, ...)
    The config needs to be instantiated with the `Config` class.
    
    In your load method, you need to instantiate you scenario at the end.
    
    ``ìnit`` argument in `__init__` allows to differenciate if it is a new
    scenario or a loaded scenario

### How to

1. Work in a `src/services/filesystem/local_scenario.py` file.
2. Test your code with `pytest test_exercise.py`

### Detailed instructions
Use property decorator and setter decorator.

* `@classmethod` is needed to create the `load` method.

* to instantiate an object in classmethod you can use:
``cls(args=args)``

* to update instance attributes you can use:
`` self.__dict__.update(self._info)``

* To hash a list of objects: 
```python
import hashlib
objects_to_hash = [one_object, another_object]
md5 = hashlib.md5()
for obj in objects_to_hash:
    md5.update(str(obj).encode("utf8"))
hash = md5.hexdigest()
```

### Solution:

* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-oop-solution/src/services/filesystem/local_scenario.py)
* Full implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/services/filesystem/scenario.py)

## Exercise 2.5 - Pipeline Iterable - (branch : origin/training/ex-pipeline-run) :

### Context

Now, you want to make your code more flexible and improve the tasks flow.
You want each task to be independent from the others and to be easily monitored. This pipeline framework
will allow you to run a sequence of operations on demand.

### Task

Imagine that you have already implemented a `Stage` object to track the stages of a run in a specific order, and a `Operator` class
in charge of executing a single step (e.g. feature_engineering, model training, prediction in a demand forecast context) of your pipeline. 
See example [here](https://github.gamma.bcg.com/pages/swe-training/training-se/pipeline/pipeline.html).

Now you need to implement the `run` method of the `Pipeline` class that will execute all operators in your pipeline.
To do so, create the `Pipeline` class that inherit from the `MetaPipeline` class (where several functionalities of your pipelines object are already available). 
Only the ``run`` method needs to be implemented.

##### Principle of the `run` method:

If the current Pipeline `Stage` is at or above an `Operator` final stage, this stage should be skipped.
`output_context` (output of the Operator call) is used as the next Operators context (if not None).
After each Operator is executed, the `current_stage` should be updated to match the Operators final_stage and the scenario stage
should be as well updated. Don't forget to save the information after each step with the `save_info()` scenario method.

You can look at the `__call__` method of the `Òperator` class in `src.tasks.operators` to see how to call an operator.
If the Pipeline runs in test mode, the `scenario` & `scenario_test` should be compared at the `current_stage` with the `compare()` scenario method.
Stops when the Pipeline's `final_stage` is reached or when the last Operator is run.

Example of utilization of the run method:
````python
from src.tasks.operators import Operator
from src.tasks.pipeline import Pipeline
from src.tasks.stages import Stage

# Define method to run in the pipeline
def method_a(scenario=None, context =None, stage=None):
    print("Start")


# Define the corresponding operator
operator_a = Operator(
    operator_id="operator_a",
    final_stage= Stage.stage_a,
    python_callable=method_a
)

# Define another method
def method_b(scenario=None, context =None, stage=None):
    print("Ends")


operator_b = Operator(
    operator_id="operator_b",
    final_stage= Stage.stage_b,
    python_callable=method_b
)

# Create the operator list, basis of the pipeline
operators_  = [ operator_a, operator_b]

#Instantiate a scenario
scenario = Scenario(input_path="./tmp", name=scenario_name, config=SERVICE.config)

# Instantiate the pipeline
myPipeline = Pipeline(
    scenario=scenario,
    scenario_test=None,
    begin_stage=Stage.stage_a,
    final_stage= Stage.stage_b,
    test=False,
    operators=operators_,
)

# Run the pipeline
myPipeline.run()
````


### How to
1. Create a `local_pipeline.py` in  `src/task` and code here.
2. Test your code with `pytest test_exercise.py`.

### Detailed instructions
 - Look at the `MetaPipeline` in `src.tasks.pipeline` code to understand the class logic.
 - Don't run the Operator if the `final_stage` of the operator has been already reached.
 - Operator method (callable object) takes as arguments, a `context`, a `scenario` and a `stage` (see above example).
 - Only operators between `begin_stage` and `final_stage` from the `Pipeline` object should be executed.
 - Leverage as much as possible the elements already implemented in the `Stage`, `Operator`, `MetaPipeline` classes

### Solution
* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-pipeline-run-solution/src/tasks/local_pipeline.py)
* Full implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/tasks/pipeline.py)

## Exercise 2.6 - Model Factory - (branch : origin/training/ex-model-factory) :

### Context

As a Data Scientist, you may want to compare different models which have different methods and structures (i.e, Random Forest vs LightGBM).
A factory pattern is a suitable tool to unify a ML model framework and ensure they all have the same methods.

### Task

1. Create an abstract MetaModel class in `src/demand_forecast/ml_model/models/local_model.py` file.

    You need to define a model factory class that will allows to define a custom made Model class `MetaModel` with some
    abstract methods `fit` and `predict`.

    `MetaModel` has to be an abstract class which is defined as  :

    ```python
    class MetaModel(ABC):

        @abstractmethod
        def abs_meth(self):
            pass

    ```

2. Create a children model class:

    You need to create new mixin Model class that inherits from a external package Class and `MetaModel`.
    Add a `__module_name__` as class attribute.
    
    You must at least create a children class called `RandomForestDemandModel` inheriting from `sklearn.ensemble.RandomForestRegressor` and the `MetaModel`.
    Set `random_forest` as `__module_name__`

3. Add dynamically a property to the Meta Model class referring to its children

    Add dynamically a property to `MetaModel` referring the module_name of the children class.
    Use `__init_subclass__` which is called when the module containing a subclass is imported.


### How to
1. Create `local_model.py` in `src/demand_forecast/ml_model/models` and code here.
2. Test your code with `pytest test_exercise.py`.


### Detailed instructions
 1. Abstract method uses `@abstractmethod` decorator
 2. Make sure the external model class comes first to let the interpreter inherit of the method required from the abstract class
 3. `__init_subclass__` will automatically do the job

 ````python
model = MetaModel.random_forest(**params)
````

### Solution
* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-model-factory-solution/src/demand_forecast/ml_model/models/local_model.py)
* Full implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/demand_forecast/ml_model/models/model.py)

## Exercise 2.7 - Context manager to profile the code - (branch : origin/training/ex-context-manager) :

### Context

As a Data Scientist, you may face computation time or memory issues along your code.
A timer is a necessary tool to identify quickly which computation takes time.
The context manager, a function tool from Python allows to implement it.

This method will be create in a Service Provider object called `ServiceProvider` defined as well as a Singleton.
In a project, it is extremely useful to have a Singleton object that allows to access to different services like:
* the log
* the config
* the file system handler
* db connection
* path manager
* ...

with a simple line of code
```
SERVICE = ServiceProvider()

SERVICE.log.info("print something")
my_parameter = SERVICE.config.my_parameter
SERVICE.fs.write(my_parameter, fmt="json") #fs like filesystem
``` 

See [here](https://github.gamma.bcg.com/pages/swe-training/training-se/services/services.html)
to have more information about services.

### Task

Create a time profiler with a context manager function and log this time at the end of each stage of the pipeline


### How to
1. Create a `local_service_provider.py` in `src/services` and code here.
2. Create a ServiceProvider class
3. Add a property called `log` to be able to use the log
4. Create a time profiler called `timer` with a context manager function and log this time at the end of each stage of the pipeline.
It should have two arguments (`context` and `task`, both strings). Format is defined with a variable fmt defined as follows:
 ````python
fmt = "\033[1m\n\n{context} - {task}: \n step completed with total wall clock duration {durations:.3f} s \n\033[0m"
````
5. Add the methods given in the detailed instructions to the class
6. Test your code with `pytest test_exercise.py`

### Detailed instructions
 `yield` method allows to "split" the script executed before the function and after the function in 
 you `context.manager`.

Add the following methods (services) to your class:
 ````python
    from .config.config_handler import ConfigHandler
    from .db.db_handler import DbHandler
    from .filesystem.filesystem_handler import FileSystemHandler

    @property
    def config(self):
        return ConfigHandler().model_config


    @property
    def db(self):
        return DbHandler()


    @property
    def fs(self):
        return FileSystemHandler()
````

Example of utilisation : 

```python
def run(**kwargs):
    pass
SERVICE = ServiceProvider()

with SERVICE.timer(context="context_id", task="task_id"):
    run(**kwargs)
```

### Solution
* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-context-manager-solution/src/services/local_service_provider.py)
* Full implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/services/service_provider.py)


## Exercise 2.8 - Decorator - (branch : origin/training/ex-decorator) :

### Context

In your project, you might need to implement several times the same actions (timer, test, ...).
In order to do it very quickly, you can use the prebuilt tool of Python, the decorator.

### Task

1. Create a decorator, called `check_dataframe`, that checks the type of the input csv fetched from the SQL database.
This decorator must also check if some columns are missing. The `Schema` object can be useful to do this kind of task.

### How to
1. Create `local_func_utils.py` in `src/utils` and code here.
2. Test your code with `pytest test_exercise.py`

### Detailed instructions
- Your decorator must take the data frame name as argument
- Return an assert statement if an error needs to be raised
- All the information to use as a reference (for the column names & types) are contained in the config file
 `data/data_fetch/type.yml` and you need to filter it accordingly to the data frame you are considering and whose name
  you use as an argument of your decorator

### Solution
* Solution: [here](https://github.gamma.bcg.com/swe-training/training-se-solution/blob/ex-decorator-solution/src/utils/local_func_utils.py)
* Full Implementation: [here](https://github.gamma.bcg.com/swe-training/training-se/blob/training-se/src/utils/func_utils.py)

# To go further in the deployment...(Optional exercises not covered by the training session)
## Exercise 2.9 - Docker image - (branch : origin/training/ex-docker-image) :

### Context

Now the model is implemented, you need to deploy it in the client infrastructure.
A way to ensure it will be easily integrated is to use Docker.

In order to get familiar with it, you will implement a docker image of the web application for the outputs.

### Task

1. You need to create the Dockerfile for the basic web app in the `/app` directory.
The Image must be based on the `python:3.6-alpine` and you need to expose the port `5000`

    At the end of the Dockerfile, a running command should launch the app.

2. Create a `local_docker-compose-app.yaml` in the repo root. Create the app service in this file :
 linked to the above dockerfile, add the ports configuration and add a volume mapping to `/app` directory. 
Then do `docker-compose -f docker-compose.yaml -f local_docker-compose-app.yaml up`, all services should run and you
should see your dashboard on `localhost:5000`.

### How to
1. Go to `app/Dockerfile` and code here.
2. Create a `local_docker-compose-app.yaml` to enrich the `docker-compose` file.
3. Do `docker-compose -f docker-compose.yaml -f local_docker-compose-app.yaml up`.
4. Check with `pytest test_exercise.py`.
5. Check your `localhost:5000`.

### Detailed instructions
 - `requirements.txt` need to be install in the Dockerfile.
 - Publish your port outside of your container with `ports` in the docker-compose file.
 - Don't forget to add a network to your service (bridge).
 - Don't forget to map the `/app` directory as a volume; the results written by the demand forecast model must be 
 dynamically updated in the web app container (otherwise the results won't be updated after the container creation)


## Exercise 2.10 - Unitest - CI configuration - (branch : origin/training/ex-ci-conf) :

### Context

Implementing a CI enables easier contributions to the code base. It is especially important for code that may be used for a long period of time, need maintenance or improvements.

You should now be familiar with the concepts of the CI. We have setup a CI (hosted on Circle CI), hooked to the 
git repository: this means that whenever someone pushes to the git repository, the CI will launch pre-defined jobs 
and return a status (Success or Failed).

Right now, the CI is not configured to launch any test.

### Task

You need to change the CI configuration and add 2 jobs:
* unit tests
* integration tests

### How to
1. Create your own branch (`git checkout -b my_branch_name`)
2. Change the CI configuration and add two jobs: "Unit tests" and "Integration tests"
3. Adapt the commands of these tests so that they launch the appropriate tests, with `pytest`
4. Commit the file & push
5. Go to https://cci.gamma.bcg.com/gh/swe-training/training-se ; under "BUILDS" you should see your commit being tested by the CI.

### Detailed instructions
1. The CI configuration is defined in .circleci/config.yml
2. Tests (unit & integration) are in the test directory
3. You should use `pytest`, e.g. `pytest test/unit_tests` will trigger all unit tests.

### Troubleshooting
If you can't log in https://cci.gamma.bcg.com/gh/swe-training/training-se, you can also create a Pull Request on GitHub (https://github.gamma.bcg.com/swe-training/training-se) and see the CI status from there.

### Takeaways
Setting up a CI is surprisingly easy with Circle CI; for more complex builds or heavier docker images, we recommend using Jenkins, but it requires its own instance (and comes at a cost), whereas to setup Circle CI, the only thing you need it access to the platform and a config.yml file. You can find documentation on confluence about these two solutions.
