"""
This script contains scenario class
"""
import hashlib
import os
import pathlib as pl
import time
import git
import pandas as pd
import yaml
from typing import Union

from src.services.config.config_handler import Config
from src.services.filesystem.container import Container
from src.services.service_provider import ServiceProviderHandler
from src.tasks.stages import Stage

SERVICE = ServiceProviderHandler()


class InvalidScenario(RuntimeError):
    """Custom exception for invalid data packs (e.g. files missing)"""


class Scenario(Container):
    """
    The Scenario object is a simple data versioning system of your runs and allows to manage your
    different scenarios by saving the corresponding data and config. It is based on a directory
    where the config, the run information  and the output data are stored.
    The scenario object has these following properties : name, locations, hash, dtcreated, stage,
    git_hash, config.
    This class allows to load directly a scenario and compare two different scenarios on :
    config, code, data, model, score,...
    """

    extension = {".pkl": "pickle", ".csv": "csv", ".yaml": "yaml"}

    def __init__(self, input_path: str = None, name: str = None,
                 config: "Config" = None,
                 init: bool = True):

        super(Scenario, self).__init__(location=pl.Path(f"{input_path}/{name}"))

        if init:
            self._config = config
            self._output = {}
            self._name = name
            self._storage_location = self.storage_location
            self._dtcreated = time.time()
            self._test = False
            self._stage = Stage.TRAINING_INIT
            self._git_hash = self.git_hash
            self._hash = self.hash
        else:
            self.__dict__.update(self._info)

    @classmethod
    def load(cls, scenario_path: str):
        """Loads a scenario from a given path, after checking it contains the required files"""
        # try:
        with open(pl.Path(scenario_path) / cls.INFO, 'r') as info:
            cls._info = yaml.safe_load(info)
        cls._config = Config(pl.Path(scenario_path) / cls.CONFIG)
        cls._storage_location = pl.Path(scenario_path)

        invalid_file = list(
            cls._check_module(cls._config, cls._storage_location,
                              cls._info['_stage']))
        if len(invalid_file) > 0:
            raise InvalidScenario(
                f"The directory: {scenario_path} is not a valid scenario,"
                f" {invalid_file} are missing")
        return cls(init=False)

    @property
    def stage(self) -> Union[str, "Stage"]:
        """Get the current stage of the scenario"""
        return self._stage

    @stage.setter
    def stage(self, stage: str):
        """Set the current stage of the scenario"""
        self._stage = stage

    @property
    def test(self) -> bool:
        """Get whether the scenario has been tested"""
        return self._test

    @test.setter
    def test(self, check):
        """Set wether the scenario has ben tested"""
        self._test = check

    @property
    def info(self):
        """Get the info dictionary of the scenario"""

        _info = {
            '_name': self._name,
            '_hash': self._hash,
            '_dtcreated': self._dtcreated,
            '_stage': self._stage,
            '_test': self._test,
            '_git_hash': self.git_hash
        }

        return _info

    @property
    def config(self):
        """Get the config of the scenario as a Config object"""
        return self._config

    @property
    def output(self):
        """get the output dictionary"""
        return self._output

    @output.setter
    def output(self, key, value):
        """Update output dictionary"""
        self._output.update({key: value})

    @property
    def location(self):
        """Get the location of the scenario (path)"""
        return self._storage_location

    @property
    def name(self):
        """Get the name of the scenario"""
        return self._name

    @property
    def dtcreated(self):
        """Get the creation date of the scenario"""
        return time.strftime("%d/%m/%Y %H:%M", time.localtime(self._dtcreated))

    @property
    def hash(self):
        """Get the hash of scenario build on the config and the commit hash"""
        objects_to_hash = [self._config, self._git_hash]
        md5 = hashlib.md5()
        for obj in objects_to_hash:
            md5.update(str(obj).encode("utf8"))
        return md5.hexdigest()

    def __str__(self):
        """Allow the str method on the class"""
        return "Scenario<{hash}, {date}> at {path}".format(hash=self._hash,
                                                           path=self._storage_location,
                                                           date=self.dtcreated)

    @property
    def git_hash(self):
        """Get the current commit hash"""
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        return sha

    def save_info(self) -> None:
        """Save the info dictionary in location / info.yml"""
        dst = self.relpath(path=Container.INFO)
        SERVICE.fs.write(self.info, dst, fmt="yaml")

    def save_config(self) -> None:
        """Save the config in location / model_config.yml"""
        dst = self.relpath(path=Container.CONFIG)
        SERVICE.fs.write(self._config.to_dict(), dst, fmt="yaml")

    def save_output(self) -> None:
        """Save the output in location / output.yml"""
        dst = self.relpath(path=Container.OUTPUT)
        SERVICE.fs.write(self._output, dst, fmt="yaml")

    def save(self) -> None:
        """save different meta info file"""
        self.save_config()
        self.save_info()
        self.save_output()

    @staticmethod
    def _check_module(config, path, stage):
        """
        Generator that checks directory hierarchy from a given path and a given stage
        It returns invalid path

        :param path:
        :param stage:
        :return: invalid file
        """
        for stage_ in Scenario.stages():
            for file_ in stage_.children:

                file_ = path / stage_.path / file_
                # Input data are not required, continue
                if stage_.name in [Stage.TRAINING_FETCHED,
                                   Stage.PREDICTION_FETCHED]:
                    if file_.suffix == ".csv":
                        continue
                if config.run_info.run_mode != "backtest" and stage_ in [
                    Stage.PREDICTION_BACKTESTINGFETCHED,
                    Stage.PREDICTION_BACKTESTED]:
                    continue
                check = file_.is_file()
                if not check:
                    yield file_

            # Stop after checking all the files up to the requested stage
            if (stage == stage_):
                break

    def is_scenario_valid(self, path):
        """Return if the scenario is valid"""
        if os.path.isfile(path / Container.INFO):
            _info = SERVICE.fs.read(path / Container.INFO, fmt="yaml")

            if len(list(self._check_module(self._config, path,
                                           _info["stage"]))) > 0:
                return False

            return True

        else:
            return False

    def compare(self, stage: "Stage", scenario: "Scenario"):
        """Compares this Scenario to another reference Scenario,
        for the given Stage.
        """

        if stage is None:
            for stage_ in Scenario.stages():
                self.compare(stage_, scenario)

        else:
            assert isinstance(scenario, Scenario), "scenario is not a scenario"
            if isinstance(scenario.stage, str):
                other_stage = scenario.get_stage(scenario.stage)
            else:
                other_stage = scenario.stage
            assert other_stage >= stage, "scenario to compare doesn't contains this stage"

            if self.config != scenario.config:
                raise Warning('Model configs are different')

            for file_ in stage.children:
                file_path = pl.Path(file_)
                if stage.name in [Stage.TRAINING_FETCHED, Stage.PREDICTION_FETCHED]:
                    if pl.Path(file_path).suffix == ".csv":
                        continue
                file_to_check = SERVICE.fs.read(
                    self.location / stage.path / file_, fmt=self.extension[file_path.suffix])
                file_checked = SERVICE.fs.read(
                    scenario.location / stage.path / file_,
                    fmt=scenario.extension[file_path.suffix])

                if isinstance(file_to_check, pd.DataFrame):
                    # equality == drop_duplicates is null
                    if len(pd.concat(
                            [file_to_check, file_checked]).drop_duplicates(
                        keep=False)) == 0:

                        SERVICE.log.info(f"Test valid for {file_}")

                    else:
                        raise InterruptedError(
                            f'Test not valid. {file_} is different with the reference scenario')

                elif file_path.suffix == '.pkl':
                    # Don't compare pkl object
                    pass

                else:
                    if file_to_check == file_checked:
                        SERVICE.log.info(f"Test valid for {file_}")
                    else:
                        raise InterruptedError(
                            f'Test not valid. {file_} is different with the reference scenario')


