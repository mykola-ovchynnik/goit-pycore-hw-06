from models import AddressBook, Record
from utils import input_error, parse_input


@input_error
def add_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    if record:
        return "Contact already exists."
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if not record:
        return "Contact does not exist."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def delete_contact(args, contacts):
    name = args[0]
    if not contacts.find(name):
        return "Contact does not exist."
    contacts.delete(name)
    return "Contact deleted."


def show_all(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join([str(record) for record in contacts.values()])


@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if not record:
        return "Contact does not exist."
    return str(record)


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "delete":
                print(delete_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case "exit" | "close":
                print("Good bye!")
                break
            case _:
                print("Invalid command")


if __name__ == "__main__":
    main()
