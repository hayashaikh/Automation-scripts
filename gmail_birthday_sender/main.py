import csv
from datetime import datetime
# File path for the CSV "Contact Book"
contact_book = 'birthdays.csv'

# prompt the user for their/sender information
while True:
    try:
        sender_eaddress = input("Enter your email address: ").strip()
        if not sender_eaddress.endswith("gmail.com") or sender_eaddress == "gmail.com":
            raise ValueError("Error:")
            # user email must contain a name before 'gmail.com' and /gmail.com"
        # print(f"Email '{sender_eaddress}' is valid.") # debug message
        break  # exit loop, email address shows valid input

    except ValueError as e:
        print(f"{e} Invalid Email! Please try again.")

# if the email is valid, the program continues + password input
sender_password = input("Enter your password: ")

# to read emails from the CSV file (user's contact book)
def read_address():
    recipients = []
    try:
        with open(contact_book, 'r', newline='', encoding='ascii') as file:
            contacts = csv.DictReader(file)  # using DictReader to access columns per contact row
            for contact in contacts:
                email = contact.get('Email', '').strip()
                name = contact.get('Name', '').strip()
                dob = contact.get('Date of Birth', '').strip()

                # to skip empty or incorrectly formatted contacts
                if not email or not name or not dob:
                    continue

                try:
                    dob_object = datetime.strptime(dob, '%Y-%m-%d').date()
                    recipients.append({'Email': email, 'Name': name, 'Date of Birth': dob_object})
                except ValueError:
                    print(f"Skip {name} ({email}): Invalid date format '{dob}', expected YYYY-MM-DD.")

    except FileNotFoundError:
        print(f"Error: The file '{contact_book}' was not found.")
    except Exception as e:
        print(f"{e}.There are no contacts in your contact book.")
        # print(f"An unexpected error occurred: {e}") debug message
    return recipients


# Function to display recipients and allow user to select one
def select_recipient(recipients):
    if not recipients:
        print("No valid recipients found in your contact book.")
        return None

    print("\nList of addresses from the Mailing List:")
    for i, recipient in enumerate(recipients, start=1):
        print(f"{i}. {recipient['Name']} ({recipient['Email']}) Birthday: {recipient['Date of Birth']}") # dont adjust!

    while True:
        try:
            choice = int(input("\nSelect a contact in your list. Enter the according number: ")) - 1
            if 0 <= choice < len(recipients):
                return recipients[choice]
            else:
                print("Invalid contact. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Read CSV/ contact book and select recipient
print("Reading Mailing List...")
recipients = read_address()
print(f"You have {len(recipients)} addresses.")

selected_recipient = select_recipient(recipients)

if selected_recipient:
    recipient_eaddress = selected_recipient['Email']
    recipient_name = selected_recipient['Name']

    # Get custom message input
    birthday_message = input(f"Enter birthday message for {recipient_name}: ")
    print(f"\n--- Ready to Send ---")
    print(f"From: {sender_eaddress}")
    print(f"To: {recipient_eaddress}")
    print(f"Subject: Happy Birthday {recipient_name}!")
    print(f"\n{birthday_message}")
    print("\n--- End of Message ---")

else:
    print("No recipient selected.")
    # ends program
