import hashlib
import getpass

password_manager={}
def create_account():
    username = getpass.getpass("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    password_manager[username] = hashlib.sha256(password.encode()).hexdigest() 
    hashed_password= hashlib.sha256(password.encode()).hexdigest()
    password_manager[username]= hashlib.sha256(password.encode()).hexdigest()
    print("Account created successfully!\n")

def login():
    username = getpass.getpass("Enter your username: ")
    password = getpass.getpass("Enter your password: ")


    hashed_password= hashlib.sha256(password.encode()).hexdigest()


    if username in password_manager and password_manager[username] == hashed_password:
        print("Login successful!\n")
        return True
    else:
        print('Invalid username or password. Give it another shot.\n')
        return False

def main():
    while True:
        print("Welcome to the Password Manager!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
           create_account()
        elif choice == '2':
            login()
        elif choice == '3':
             print("Bye bye, Password Manager. Goodbye!")
             break
        else:
             print("Invalid choice. Think harder.\n")

if __name__==  "__main__":
    main()

