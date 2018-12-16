
from typing import Callable, Union
import argparse
import json
import os

def parse_arguments(config_file: Union[str, None]) -> object:
    execution_path = os.getcwd()
    config_file_to_load = config_file if config_file is not None else "config/arguments.json"
    config_file_parser = argparse.ArgumentParser(add_help=False)

    config_file_parser.add_argument(
        "--defaults",
        type=str,
        help="sets where defaults are read from",
        default="config/defaults.json")
    config_file_parser.add_argument(
        "--self-info",
        type=str,
        help="sets file containing information like version for your program",
        default="config/self.json")

    builtin_flags, remaining_args = config_file_parser.parse_known_args()
    defaults_file, self_file  = builtin_flags.defaults, builtin_flags.self_info
    defaults, self_info = [load_configuration_json(execution_path, file_name) for file_name in [defaults_file, self_file]]

    argument_parser = argparse.ArgumentParser(
        parents=[config_file_parser],
        **self_info)
    argument_parser.set_defaults(**defaults)

    with open(f"{execution_path}/{config_file_to_load}") as arguments_file:
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
    except FileNotFoundError:
        return {}
