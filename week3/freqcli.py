#!/usr/bin/python3
# A script template
# Licensed under the MIT License (https://opensource.org/license/mit)
# ARI-20130930

# Set up initial variables and imports
import sys
import string

def is_vowel(char):
    return char in "aeiou"

def count_letters(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read().lower()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    letter_counts = {}

    for char in text:
        if char in string.ascii_lowercase:
            if char in letter_counts:
                letter_counts[char] += 1
            else:
                letter_counts[char] = 1

    return letter_counts

def print_counts(counts):
    for letter in sorted(counts.keys()):
        print(f"{letter} - {counts[letter]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python freqcli.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    letter_counts = count_letters(filename)
    print_counts(letter_counts)

if __name__ == "__main__":
    main()
