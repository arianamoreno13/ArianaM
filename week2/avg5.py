#!/usr/bin/python3
# A script template week 2
# Licensed under the MIT License (https://opensource.org/license/mit)
# ARI-20130930

# Set up initial variables and imports
import sys

# Script/Library Functions
def calculate_average(numbers):
    """Cal the avg of a list of #s to two decimal places."""
    return round(sum(numbers) / len(numbers), 2)
def main():
    if len(sys.argv) != 6:
        print("Usage: ./avg5.py num1 num2 num3 num4 num5")
        print("All inputs must be positive numbers.")
        sys.exit(1)
    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
        if not all(n > 0 for n in numbers):
            raise ValueError("All numbers must be positive.")
    except ValueError:
        print("Usage: ./avg5.py num1 num2 num3 num4 num5")
        print("All inputs must be positive numbers.")
        sys.exit(1)
    
    average = calculate_average(numbers)
    print(f"Average: {average:.2f}")

# Run main() if script called directly, else use as a library to be imported
if __name__ == '__main__':
    main()
  
