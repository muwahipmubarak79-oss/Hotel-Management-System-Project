# users/models.py
users = []

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = {
        "username": username,
        "password": password
    }

    users.append(user)
    print("User registered successfully!")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return

    print("Invalid username or password")

def show_users():
    if len(users) == 0:
        print("No users found")
    else:
        for i, user in enumerate(users, 1):
            print(i, user["username"])

def menu():
    while True:
        print("\n--- USER MANAGEMENT SYSTEM ---")
        print("1. Register")
        print("2. Login")
        print("3. Show Users")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            show_users()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option")

menu()