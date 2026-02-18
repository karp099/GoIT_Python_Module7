from datetime import datetime, date, timedelta
import classes as c

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "We don't have an entry with that name."
        except IndexError:
            return "That's a bit too far! Please pick a valid number."
        except TypeError:
            return "You didn't gave information."
        except AttributeError:
            return "Contact not found."

    return inner



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def string_to_date(date_string):
    return datetime.strptime(date_string, "%d.%m.%Y").date()


def date_to_string(date):
    return date.strftime("%d.%m.%Y")


def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()

    for user in users:
        birthday_this_year = user["birthday"].replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year+1)
        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)
            
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
    return upcoming_birthdays


@input_error
def add_contact(args, book: c.AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = c.Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message



@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f"Contact {name} updated"


@input_error
def print_phone(args, book):
    name = args[0]
    record = book.find(name)
    phones_str = "; ".join(p.value for p in record.phones)
    return f"Contact {record.name.value}: {phones_str}"


@input_error
def print_all(book):
    if not book:
        return "Book is empty."
    return str(book)

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added"

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    return f"Birthday for {name}: {record.birthday.value}"

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays next week."
    res = ""
    for user in upcoming:
        res += f"{user['name']}: {user['congratulation_date']}\n"
    return res.strip()


commands_menu = """
Hello! 
All commands:
 
1) add [name] [phone] - to add new contact with name and phone number
2) all - to show all saved contacts
3) change [name] [old_number] [new_phone] - to change saved contact 
4) close or exit - to close the program
5) help - to show this menu
6) phone [name] - to show phone
7) add-birthday [name][dd.mm.yyyy] - to add new birthday to your contact
8) show-birthday [name] - to show birthday to contact
9) birthdays - to show all birthdays in next 7 days 
"""

banner = r""" 
   _____                .__          __                 __    ___.           __         ___    
  /  _  \   ______ _____|__| _______/  |______    _____/  |_  \_ |__   _____/  |_   /\  \  \   
 /  /_\  \ /  ___//  ___/  |/  ___/\   __\__  \  /    \   __\  | __ \ /  _ \   __\  \/   \  \  
/    |    \\___ \ \___ \|  |\___ \  |  |  / __ \|   |  \  |     | \_\ (  <_> )  |    /\    )  ) 
\____|__  /____  >____  >__/____  > |__| (____  /___|  /__|    |___  /\____/|__|    \/   /  /  
        \/     \/     \/        \/            \/     \/            \/                   /__/   
"""
