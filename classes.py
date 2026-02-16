from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        value = str(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_phone(self, phone_number):
        new_phone_number = Phone(phone_number)
        self.phones.append(new_phone_number)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
            return
        raise ValueError("Phone not found")

    def edit_phone(self, old_number, new_number):
        old_phone = self.find_phone(old_number)
        if old_phone:
            idx_old_phone = self.phones.index(old_phone)
            self.phones[idx_old_phone] = Phone(new_number)
            return
        raise ValueError("Phone not found")
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        
    def get_upcoming_birthdays(self):
        from functions import get_upcoming_birthdays, string_to_date
        prepared_users = []
        for record in self.data.values():
            if record.birthday:
                prepared_users.append({
                    "name": record.name.value,
                    "birthday": string_to_date(record.birthday.value)
                })
        return get_upcoming_birthdays(prepared_users)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
