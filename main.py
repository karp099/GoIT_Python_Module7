import functions as func


def main():
    book = func.load_data()
    print(func.banner)
    print("Welcome to the assistant bot!")
    print(func.commands_menu)
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = func.parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(func.add_contact(args, book))
        elif command == "help":
            print(func.commands_menu)
        elif command == "phone":
            print(func.print_phone(args, book))
        elif command == "change":
            print(func.change_contact(args, book))
        elif command == "all":
            print(func.print_all(book))
        elif command == "add-birthday":
            print(func.add_birthday(args, book))
        elif command == "show-birthday":
            print(func.show_birthday(args, book))
        elif command == "birthdays":
            print(func.birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
