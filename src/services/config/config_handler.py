"""
This script contains configuration file handler
"""

import collections
import importlib
import logging
import os

import yaml


class ConfigHandler:
    """
    Class to handle different config file.
    Each file from the yaml directory will be instantiate as a Config object and set as an attribute
    of the ConfigHandler object
    """
    @staticmethod
    def __new__(cls, yaml_directory=None):
        """
        Singleton for config handler.

        All files from the yaml _directory are an attribute of the ConfigHandler Class.
        This Attribute com from the Config class below, inherited from collections.Mapping class

        :param yaml_directory:
        :return:
        """
        if not hasattr(cls, '_config'):
            cls._config = super(ConfigHandler, cls).__new__(cls)
            if yaml_directory is not None:
                if not os.path.isdir(yaml_directory):
                    raise FileNotFoundError(f'{yaml_directory} not found')
                logging.info(f"Loading YAML from {yaml_directory}")
                (_, __, filenames) = next(os.walk(yaml_directory))

                for file_ in filenames:
                    setattr(
                        cls._config,
                        str(file_.split('.')[0]),
                        Config(yaml_directory / file_),
                    )

            else:
                raise RuntimeError(
                    "ConfigHandler need a directory path for its first instantiation")

        return cls._config


class Config(collections.Mapping):
    """
    Config class wrapped in a Box.

    The method is_config_valid allow to check the config based on a schema
    """

    def __init__(self, yaml_file):
        # read only mode
        from box import Box
        with open(yaml_file, "r") as f:
            self.__data = Box(yaml.load(f, Loader=yaml.SafeLoader), frozen_box=True)
        sc = importlib.import_module("src.services.config.config_schema")
        self.is_config_valid(getattr(sc, yaml_file.stem))
        self._initialized = True

    # to be picklable
    def __getstate__(self):
        return self.__data

    def __setstate__(self, state):
        self.__data = state

    def __getitem__(self, item):
        return self.__data[item]

    def __getattr__(self, item):
        return self.__data[item]

    def __setattr__(self, key, value):
        if self.__dict__.get('_initialized'):
            raise Exception("Attribute is Read-Only")
        super().__setattr__(key, value)

    def __delattr__(self, item):
        raise Exception('Cannot delete attribute')

    def __iter__(self):
        # just forward to the inner container
        return iter(self.__data)

    def __len__(self):
        # just forward to the inner container
        return len(self.__data)

    # valid the model configuration
    def is_config_valid(self, schema) -> bool:
        """Check if the config is valid with schema object"""
        return schema.validate(self.__data)

    def to_dict(self):
        """return data as a dictionary"""
        return self.__data.to_dict()
