#!/usr/bin/python3
# A script template
# Licensed under the MIT License (https://opensource.org/license/mit)
# ARI-20130930

# Set up initial variables and imports
import sys
import string

def is_vowel(char):
    return char in 'aeiou'

def count_letters(filename):
    counts = {}

    try:
        with open(filename, 'r') as file:
            text = file.read().lower()
            for char in text:
                if char in string.ascii_lowercase:
                    if char in counts:
                        counts[char] += 1
                    else:
                        counts[char] = 1
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    return counts

def print_results(counts):
    vowels = {k: v for k, v in counts.items() if is_vowel(k)}
    consonants = {k: v for k, v in counts.items() if not is_vowel(k)}

    for k in sorted(vowels):
        print(f"{k} - {vowels[k]}")
    for k in sorted(consonants):
        print(f"{k} - {consonants[k]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 frequency.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    counts = count_letters(filename)
    print_results(counts)

if __name__ == "__main__":
    main()


