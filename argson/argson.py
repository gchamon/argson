
from typing import Callable, Union, Tuple, List
import argparse
import json
import os


def parse_file_and_arguments(config_file: Union[str, None],
                             self_file: str = "config/self.json",
                             defaults_file: str = "config/defaults.json",
                             working_dir: str = os.getcwd(),
                             no_builtins: bool = False,
                             verbose: bool = False) -> object:
    argument_parser, remaining_args = parse_config_file(config_file,
                                                        self_file,
                                                        defaults_file,
                                                        working_dir,
                                                        no_builtins,
                                                        verbose)

    arguments = argument_parser.parse_args(remaining_args)
    return arguments


def parse_config_file(config_file: Union[str, None],
                      self_file: str = "config/self.json",
                      defaults_file: str = "config/defaults.json",
                      working_dir: str = os.getcwd(),
                      no_builtins: bool = False,
                      verbose: bool = False) -> Tuple[argparse.ArgumentParser, List[str]]:
    builtin_parser, builtin_flags, remaining_args = parse_builtins(no_builtins,
                                                                   defaults_file)

    if no_builtins is False:
        defaults_file = builtin_flags.defaults

    defaults, self_info = [load_configuration_json(working_dir, file_name, verbose)
                           for file_name in [defaults_file, self_file]]
    argument_parser = get_argument_parser(
        builtin_parser, self_info, defaults, working_dir, config_file)
    return argument_parser, remaining_args


def parse_builtins(no_builtins, default_defaults_file) -> Tuple[argparse.ArgumentParser, object, List[str]]:
    config_file_parser = argparse.ArgumentParser(add_help=False)
    if no_builtins is False:
        config_file_parser.add_argument(
            "--defaults",
            type=str,
            help="sets where defaults are read from",
            default=default_defaults_file)

    builtin_flags, remaining_args = config_file_parser.parse_known_args()
    return config_file_parser, builtin_flags, remaining_args


def get_argument_parser(builtin_parser, self_info, defaults, load_path, config_file) -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(parents=[builtin_parser],
                                              **self_info)
    argument_parser.set_defaults(**defaults)

    arguments_filename = config_file if config_file is not None else "config/arguments.json"
    arguments_dict = load_configuration_json(load_path, arguments_filename, strict=True)

    for argument_config in arguments_dict:
        arg_flags = argument_config.pop("args", None)
        argument_parser.add_argument(
            *arg_flags, **argument_config)

    return argument_parser


def load_configuration_json(path, json_file, verbose: bool = False, strict: bool = False) -> dict:
    path_to_file = f"{path}/{json_file}"
    try:
        with open(path_to_file) as configuration_file:
            return json.load(configuration_file)
    except (FileNotFoundError, IsADirectoryError) as e:
        if strict:
            raise e
        if verbose:
            message = ''
            if isinstance(e, FileNotFoundError):
                message = f"cannot load file '{path_to_file}'"
            else:
                message = f"cannot load the directory '{path}' as file"
            print(f"[WARNING] {message}")
        return {}
