import base64
import json
import os
from getpass import getpass

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

SALT_FILE = "salt.bin"
VAULT_FILE = "vault.json"


def get_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as file:
            return file.read()

    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as file:
        file.write(salt)

    return salt


def make_key(master_password, salt):
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=2**16,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode("utf-8")))


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}

    with open(VAULT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_vault(vault):
    with open(VAULT_FILE, "w", encoding="utf-8") as file:
        json.dump(vault, file, indent=2)


def add(fer):
    name = input("Enter the site name: ").strip()
    url = input("Enter the site URL: ").strip()
    email = input("Enter the email: ").strip()
    password = input("Enter the Password: ").strip()

    vault = load_vault()
    vault[name] = {
        "url": url,
        "email": email,
        "password": fer.encrypt(password.encode("utf-8")).decode("utf-8"),
    }
    save_vault(vault)
    print("Password added.")


def view(fer):
    vault = load_vault()
    if not vault:
        print("No passwords saved yet.")
        return

    for name, data in vault.items():
        decrypted = fer.decrypt(data["password"].encode("utf-8")).decode("utf-8")
        print(f"{name} | {data['url']} | {data['email']} | Password: {decrypted}")


def main():
    master_password = getpass("Enter master password: ")
    salt = get_salt()
    key = make_key(master_password, salt)
    fer = Fernet(key)

    while True:
        print("1. Add a new Password")
        print("2. View existing Passwords")
        print("Enter q to quit")
        mode = input("> ").strip().lower()

        if mode == "q":
            print("Come Back Again :)")
            break

        if mode == "1":
            add(fer)
        elif mode == "2":
            view(fer)
        else:
            print("Invalid mode")


if __name__ == "__main__":
    main()
