#!/usr/bin/env python3
# dates.py

from datetime import datetime, timedelta

def main():
    try:
        # Prompt for birthdate
        birthdate_input = input("Enter your birthdate (mm-dd-yyyy): ")
        birthdate = datetime.strptime(birthdate_input, "%m-%d-%Y")
    except ValueError:
        print("Invalid birthdate format. Please use mm-dd-yyyy.")
        return

    try:
        # Prompt for number of days
        days_input = input("Enter the number of days to add: ")
        days_to_add = int(days_input)
        if days_to_add <= 0:
            raise ValueError
    except ValueError:
        print("Invalid number of days. Please enter a positive integer.")
        return

    # Add days
    future_date = birthdate + timedelta(days=days_to_add)

    # Output the result
    print(f"\nA person born on {birthdate.strftime('%B %d, %Y')} will reach {days_to_add} days old on {future_date.strftime('%B %d, %Y')}.")

if __name__ == "__main__":
    main()
