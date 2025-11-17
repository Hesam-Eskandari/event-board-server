import pathlib


class PathHelper:

    @staticmethod
    def get_root_path() -> pathlib.Path:
        return pathlib.Path().absolute().parent
