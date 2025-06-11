#!/usr/bin/env python3

import sys

def calculate_average(numbers):
    #Calculate the avg of a list of pos(+) #s, rounded to two decimal places.
    return round(sum(numbers) / len(numbers), 2)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./avgn.py num1 num2 ... numN")
        print("All inputs must be positive numbers.")
        sys.exit(1)

    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
        if not all(n > 0 for n in numbers):
            raise ValueError
    except ValueError:
        print("Usage: ./avgn.py num1 num2 ... numN")
        print("All inputs must be positive numbers.")
        sys.exit(1)

    average = calculate_average(numbers)
    print(f"Average: {average:.2f}")

if __name__ == '__main__':
    main()
