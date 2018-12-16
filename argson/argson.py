
from typing import Callable, Union
import argparse
import json
import os

def parse_arguments(config_file: Union[str, None],
                    self_file: str = "config/self.json",
                    working_dir: Union[str, None] = None,
                    no_builtins: bool = False) -> object:
    load_path = os.getcwd() if working_dir is None else working_dir
    config_file_to_load = config_file if config_file is not None else "config/arguments.json"
    config_file_parser = argparse.ArgumentParser(add_help=False)

    argument_parser = None
    remaining_args = []
    if no_builtins is False:
        config_file_parser.add_argument(
            "--defaults",
            type=str,
            help="sets where defaults are read from",
            default="config/defaults.json")

    builtin_flags, remaining_args = config_file_parser.parse_known_args()
    defaults_file  = builtin_flags.defaults if no_builtins is False else ''
    defaults, self_info = [load_configuration_json(load_path, file_name) for file_name in [defaults_file, self_file]]

    argument_parser = argparse.ArgumentParser(
        parents=[config_file_parser],
        **self_info)
    argument_parser.set_defaults(**defaults)
    with open(f"{load_path}/{config_file_to_load}") as arguments_file:
        arguments = json.load(arguments_file)
        for argument_config in arguments:
            arg_flags = argument_config.pop("args", None)
            argument_parser.add_argument(
                *arg_flags, **argument_config)

    arguments = argument_parser.parse_args(remaining_args)
    return arguments


def load_configuration_json(path, json_file):
    try:
        with open(f"{path}/{json_file}") as configuration_file:
            return json.load(configuration_file)
    except (FileNotFoundError, IsADirectoryError):
        return {}
