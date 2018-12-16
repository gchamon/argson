import argson
import os
PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    argson.parse_file_and_arguments('config/example.json', self_file='config/self-example.json', working_dir=PATH)
    print("err... you probably want to run this file with the flag '--help' to see the effects of self_file flag")


if __name__ == "__main__":
    main()
