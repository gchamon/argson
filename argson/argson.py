
from typing import Callable, Union, Tuple, List
import argparse
import json
import os


def parse_file(config_file: Union[str, None],
               self_file: str = "config/self.json",
               working_dir: Union[str, None] = None,
               no_builtins: bool = False,
               verbose: bool = False) -> Tuple[argparse.ArgumentParser, List[str]]:
    def load_configuration_json(path, json_file):
        path_to_file = f"{path}/{json_file}"
        try:
            with open(path_to_file) as configuration_file:
                return json.load(configuration_file)
        except (FileNotFoundError, IsADirectoryError) as e:
            if verbose:
                message = ''
                if isinstance(e, FileNotFoundError):
                    message = f"cannot load file '{path_to_file}'"
                else:
                    message = f"cannot load the directory '{path}' as file"
                print(f"[WARNING] {message}")
            return {}

    load_path = os.getcwd() if working_dir is None else working_dir
    config_file_to_load = config_file if config_file is not None else "config/arguments.json"
    config_file_parser = argparse.ArgumentParser(add_help=False)

    argument_parser = None
    remaining_args = []
    default_defaults_file = "config/defaults.json"
    if no_builtins is False:
        config_file_parser.add_argument(
            "--defaults",
            type=str,
            help="sets where defaults are read from",
            default=default_defaults_file)

    builtin_flags, remaining_args = config_file_parser.parse_known_args()
    defaults_file = builtin_flags.defaults if no_builtins is False else default_defaults_file
    defaults, self_info = [load_configuration_json(
        load_path, file_name) for file_name in [defaults_file, self_file]]

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

    return argument_parser, remaining_args


def parse_file_and_arguments(config_file: Union[str, None],
                             self_file: str = "config/self.json",
                             working_dir: Union[str, None] = None,
                             no_builtins: bool = False,
                             verbose: bool = False) -> object:
    argument_parser, remaining_args = parse_file(config_file,
                                 self_file,
                                 working_dir,
                                 no_builtins,
                                 verbose)

    arguments = argument_parser.parse_args(remaining_args)
    return arguments
