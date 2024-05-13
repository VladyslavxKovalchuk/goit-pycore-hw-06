from pathlib import Path
from model.addressBook import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            if len(args) > 0:
                return err.args[0]
            else:
                return err.__doc__
        except KeyError:
            return "Contact does not exist."
        except IndexError:
            return "Arguments are required."

    return inner


def get_contact_filepath():
    datapath = Path("./data/contacts.dat")
    if not datapath.exists():
        with open(datapath, "w+"):
            return datapath

    return datapath


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("invalid params. The correct is: add ContactName PhoneNumber")

    name, *phones = args
    newrecord = Record(name)
    for phone in phones:
        newrecord.add_phone(phone)

    book.add_record(newrecord)
    return "Contact added."


@input_error
def add_phone(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: addphone ContactName PhoneNumber"
        )

    name, phone = args
    record: Record = book.find(name)
    record.add_phone(phone)
    return "Phone added."


@input_error
def remove_phone(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: removephone ContactName PhoneNumber"
        )

    name, phone = args
    record: Record = book.find(name)
    record.remove_phone(phone)
    return "Phone removed."


@input_error
def update_phone(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError(
            "invalid params. The correct is: updatephone ContactName oldphone newphone"
        )

    name, oldphone, newphone = args
    record: Record = book.find(name)
    record.edit_phone(oldphone, newphone)
    return "Phone updated."


@input_error
def remove_contact(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: remove ContactName")

    name = args[0]
    book.delete(name)
    return "Contact removed."


@input_error
def show_contacts(book):
    book.print()


def get_allowed_commands():
    return [
        "close",
        "exit",
        "add",
        "remove",
        "show",
        "phone",
        "addphone",
        "removephone",
        "updatephone",
        "findbyphone",
        "findbyname",
    ]


@input_error
def get_phones(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: phone ContactName")
    name = args[0]

    record = book.find(name)
    return f"{'; '.join(p.value for p in record.phones)}"


@input_error
def find_contacts(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: findbyphone phone")
    phone = args[0]

    records = book.find_record_by_phone(phone)
    for rec in records:
        print(rec)


@input_error
def find_bypattern(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: findbyname namepart")
    name = args[0]

    records = book.find_record_by_name(name)
    for rec in records:
        print(rec)


def main():
    print("Welcome to the assistant bot!")
    book = AddressBook()
    book.load_from_file(get_contact_filepath())
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close":
                print("Good bye!")
                book.save_to_file(get_contact_filepath())
                break
            case "exit":
                print("Good bye!")
                book.save_to_file(get_contact_filepath())
                break
            case "add":
                print(add_contact(args, book))
            case "remove":
                print(remove_contact(args, book))
            case "show":
                show_contacts(book)
            case "phone":
                print(get_phones(args, book))
            case "addphone":
                print(add_phone(args, book))
            case "removephone":
                print(remove_phone(args, book))
            case "updatephone":
                print(update_phone(args, book))
            case "findbyphone":
                find_contacts(args, book)
            case "findbyname":
                find_bypattern(args, book)
            case "help":
                print("Allowed commands:")
                print(get_allowed_commands())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
