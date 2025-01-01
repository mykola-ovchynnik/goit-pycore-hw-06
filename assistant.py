from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.__phones = []

    def add_phone(self, phone):
        self.__phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.__phones = [p for p in self.__phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.__phones:
            if p.value == phone:
                return p
        return None

    @property
    def phones(self):
        return self.__phones

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.__phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact does not exist."
        except ValueError as e:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return inner


def parse_input(user_input):
    if not user_input.strip():
        return None, []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


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
