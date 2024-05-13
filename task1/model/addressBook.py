from collections import UserList
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.value = name

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, phone):
        self.setphone(phone)

    def __str__(self):
        return str(self.value)

    def setphone(self, phone):
        if not re.match(r"^\d{10}$", phone):
            raise ValueError("phone must be in XXXXXXXXXX format")
        self.value = phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if type(phone) is Phone:
            self.phones.append(phone)
        else:
            if len(list(filter(lambda x: x.value == phone, self.phones))) > 0:
                raise ValueError(f"Phone no {phone} already exist.")
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phones = list(filter(lambda x: x.value == phone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {phone} is not found.")
        self.phones = list(filter(lambda x: x.value != phone, self.phones))

    def edit_phone(self, oldphone, newphone):
        phones = list(filter(lambda x: x.value == oldphone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {oldphone} is not found.")
        phones[0].setphone(newphone)

    def find_phone(self, phone):
        phones = list(filter(lambda x: x.value == phone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {phone} is not found.")
        return phones[0]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserList):
    def add_record(self, record):
        if (
            len(list(filter(lambda x: x.name.value == record.name.value, self.data)))
            > 0
        ):
            raise ValueError(f"Contact name {record.name.value} already exist.")
        self.append(record)

    def delete(self, contactname):
        self.data = list(filter(lambda x: x.name.value != contactname, self.data))

    def find(self, contactname):
        foundlist = list(filter(lambda x: x.name.value == contactname, self.data))
        if len(foundlist) == 0:
            raise ValueError(f"Contact name {contactname} is not found.")
        return foundlist[0]

    def load_from_file(self, path):
        with open(path, "r") as file:
            for contactline in file.readlines():
                rec = Record(contactline.split(";")[0])
                phones = contactline.split(";")
                phones.pop(0)
                for phone in phones:
                    rec.add_phone(phone.strip())
                self.add_record(rec)

    def save_to_file(self, path):
        with open(path, "w") as file:
            for record in self.data:
                file.write(
                    f"{record.name.value};{'; '.join(p.value for p in record.phones)}\n"
                )

    def find_record_by_name(self, name: str):
        foundlist = list(filter(lambda x: x.name.value.__contains__(name), self.data))
        return foundlist

    def find_record_by_phone(self, phone: str):
        foundlist = list(
            filter(
                lambda x: len(list(filter(lambda y: y.value == phone, x.phones))) != 0,
                self.data,
            )
        )
        return foundlist

    def print(self):
        for rec in self.data:
            print(rec)
