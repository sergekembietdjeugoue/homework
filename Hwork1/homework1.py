from datetime import datetime

def birthday_card():
    print("Welcome to the birthday card generator")
    print("Please provide the following details:\n")

# collect user input

recipient_name = input("Enter the recipient's name: ")
year_of_birth = int(input("Enter the recipient's year of birth (YYYY): "))
personalized_message = input("Enter a short personalized message: ")
sender_name = input("Enter your name: ")

# calculating age

current_year = datetime.now().year
age = current_year - year_of_birth

# generate birthday card

print("\n" + "="*50)
print(f"🎂 Happy Birthday {recipient_name}! 🎂\n")
print(f"{recipient_name}, let's celebrate your {age} years of awesomeness!")
print(f"Wishing you a day filled with joy and laughter as you turn {age}!\n")
print(f"{personalized_message}\n")
print(f"With love and best wishes,\n{sender_name}")
print("="*50)

# Run the program
birthday_card()