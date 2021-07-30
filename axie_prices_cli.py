""" CLI to add new data
"""
from axie_prices_cli_factory import factory

def print_welcome():
    print('Welcome to the axie price json interactor')

def print_modes():
    print()

    modes = {
        '[L]ist': 'Lists all the different types of documented axie',
        '[A]dd': 'Add a known sale to the document'
    }
    for k in modes:
        v = modes[k]
        print(format('%.20s -> %.100s', k, v))

    print()

def wrapped_mode_input():
    mode = input('Mode: ')
    return factory(mode.lower())

def start_cli():
    print_welcome()
    while True:
        print_modes()
        mode_inst = wrapped_mode_input()
        if mode_inst:
            mode_inst.run()
        else:
            print('Invalid Mode')
            factory('l').run()

if __name__ == '__main__':
    start_cli()