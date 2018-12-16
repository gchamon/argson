import argson
import os
PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    arguments = argson.parse_file_and_arguments('config/example.json', self_file='config/self-example.json', working_dir=PATH)

    if arguments.test is True:
        print("test flag set")
    else:
        print("test flag not set")


if __name__ == "__main__":
    main()
