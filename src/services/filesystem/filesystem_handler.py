import os
import pathlib as pl
from shutil import copyfile

from .read_service import DataReadService
from .write_service import DataWriteService


class FileSystemHandler:
    """
    Class that defines file system handler
    """
    def __init__(self):
        self._read_service = DataReadService()
        self._write_service = DataWriteService()

    @staticmethod
    def exists(path: str) -> bool:
        """
        Check if file exist under remote folder
        """
        return os.path.exists(path)

    @staticmethod
    def copy(path_from: str, dst: pl.Path):
        """
        Copy a file to destination
        """

        os_path = dst
        dir_path = os_path.parent

        # Create dir if not exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        copyfile(path_from, os_path)

    def write(self, obj, dst, fmt="csv", **write_kwargs):
        """Utility to write objects to the file system, using the DataWriteService"""
        # Get the function that generates the output
        func = getattr(self._write_service, fmt, None)
        if func is None:
            raise NameError("Format %s not recognized" % fmt)

        # Get the relative path
        pl.Path(dst.parent).mkdir(parents=True, exist_ok=True)

        return func(
            obj,
            dst,
            **write_kwargs,
        )

    def read(self, dst, fmt="csv", **read_kwargs):
        """Utility to read objects from the file system, using the DataWriteService"""
        # Get the function that reads from the fs
        func = getattr(self._read_service, fmt, None)
        if func is None:
            raise NameError("Format %s not recognized" % fmt)

        return func(
            dst,
            **read_kwargs,
        )
