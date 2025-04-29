#!/usr/bin/python3
# Script to compare a number to 10.
# Licensed under the MIT License (https://opensource.org/license/mit)
# Ski-20250206: initial version

# Initial variables and imports
import sys
NUMBER10 = 10

# Script/Library Functions
def main():
    """ Get input and compare a number to 10"""
    while True:
        var = input('Enter a number: ')
        
        if valid(var):
            var_int = int(var)
            if var < NUMBER10:
            print(var + ' is larger than 10')
            elif var > NUMBER10:
                print(var + ' is less than 10')
            else:
                print var + ' equals 10'
        all_done = input('Enter Y if all done, anything else to continue? ')
        if all_done == 'Y':
            break

def valid(x):
    try:
        var_int = int(x)
        return 0
    except ValueError:
        usage()
        return 1

def usage():
    print(" ")
    print( You must enter an integer at the prompt )
    sys.exit()

# Run main() if script called directly, else use as library to be imported
if __name__ == '__main__':
    main()
