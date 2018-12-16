import argson

def main():
    arguments = argson.parse_arguments('examples/config/example.json')

    if arguments.test is True:
        print("test flag set")
    else:
        print("test flag not set")


if __name__ == "__main__":
    main()
