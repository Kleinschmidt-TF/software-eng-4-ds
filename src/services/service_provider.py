"""
This script contains pipeline service provider
"""

import contextlib
import logging
import pathlib
import time

from .config.config_handler import ConfigHandler
from .db.db_handler import DbHandler
from .filesystem.filesystem_handler import FileSystemHandler


class ServiceProvider:
    """
    Class containing main service provider :
        - access to configuration file
        - ability to log
        - database connection
        - access to filesystem
    """

    @property
    def config(self):
        """
        Return the model config as Config object.
        The value of the config can be get with a getattr method, i.e name = self.config.name

        :return: A Config object
        """
        return ConfigHandler(
            yaml_directory=pathlib.Path(__file__).resolve().parents[2] / "configs").model_config

    @property
    def log(self):
        """
        Return the logger of the module.

        :return:
        """
        return logging.getLogger(__name__)

    @property
    def db(self):
        """
        Return the DbHandler object.

        :return: The DbHandler object
        """
        return DbHandler()

    @property
    def fs(self):
        """
        Return the FileSystemHandler object of the module.
        This object allows to write and read a file with self.fs.write() and self.fs.read()

        :return: The FileSystemHandler object
        """
        return FileSystemHandler()

    @contextlib.contextmanager
    def timer(self, context: str, task: str,
              fmt: str = "\033[1m\n\n{context} - {task}: \n step completed with total wall clock duration {durations:.3f} s \n\033[0m",
              ):
        """To enter before a callable using 'with'.

        :param srv: ServiceProvider instance, to use for logs
        :param context: task context
        :param task: task name
        :param format: format to use to display the task duration
        """
        start = time.time()
        yield
        self.log.info(
            fmt.format(
                context=context,
                task=task,
                durations=(time.time() - start),
            ),
        )


class ServiceProviderHandler:  # pylint: disable=no-member
    """
    Singleton for the Service Provider
    """

    @staticmethod
    def __new__(cls):
        """
        Singleton for service provider.

        Since every attribute in the service provider is controlled by the configuration,
        it isn't necessary to instantiate the ServiceProvider multiple times.
        """
        if not hasattr(cls, "_srv_prov"):
            cls._srv_prov = ServiceProvider()
        return cls._srv_prov
