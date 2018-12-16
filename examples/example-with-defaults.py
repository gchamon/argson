import argson
import os
PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    arguments = argson.parse_file_and_arguments('config/example.json', defaults_file='config/example.defaults.json', working_dir=PATH)
    print(arguments.string_to_print)


if __name__ == "__main__":
    main()
