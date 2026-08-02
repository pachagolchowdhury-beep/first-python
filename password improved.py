import base64
import getpass
import json
import os
import re
from hashlib import sha256
from pathlib import Path

from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent
VAULT_FILE = BASE_DIR / "vault.json"
KEY_FILE = BASE_DIR / "secret.key"


def create_master_password():
    print("\n🔐 FIRST TIME SETUP")
    print("=" * 40)
    print("Password requirements:")
    print("- At least 8 characters")
    print("- At least 1 uppercase letter")
    print("- At least 1 lowercase letter")
    print("- At least 1 number")
    print("- At least 1 special character")
    print("=" * 40)

    while True:
        master = getpass.getpass("Create master password: ")
        if not master:
            print("Password cannot be empty!\n")
            continue
        if len(master) < 8:
            print("Password must be at least 8 characters!\n")
            continue
        if not re.search(r"[A-Z]", master):
            print("Password must have at least 1 uppercase letter!\n")
            continue
        if not re.search(r"[a-z]", master):
            print("Password must have at least 1 lowercase letter!\n")
            continue
        if not re.search(r"[0-9]", master):
            print("Password must have at least 1 number!\n")
            continue
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};:'\",.<>/?\\|`~]", master):
            print("Password must have at least 1 special character!\n")
            continue

        confirm = getpass.getpass("Confirm master password: ")
        if master != confirm:
            print("Passwords don't match!\n")
            continue

        print("Password is strong!")
        return master


def derive_key(master_password):
    return base64.urlsafe_b64encode(sha256(master_password.encode("utf-8")).digest())


def get_fernet(master_password):
    return Fernet(derive_key(master_password))


def load_vault(path=VAULT_FILE):
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def save_vault(data, path=VAULT_FILE):
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


class PasswordManager:
    def __init__(self, master_password=None):
        self.master_password = master_password
        self.vault = load_vault()
        self.fernet = get_fernet(master_password) if master_password else None

    def set_master_password(self, master_password):
        self.master_password = master_password
        self.fernet = get_fernet(master_password)
        with KEY_FILE.open("wb") as fh:
            fh.write(derive_key(master_password))
        print("Master password set.")

    def add_entry(self, site, username, password):
        if not self.fernet:
            raise RuntimeError("Set a master password first.")

        encrypted_password = self.fernet.encrypt(password.encode("utf-8")).decode("utf-8")
        self.vault[site] = {
            "username": username,
            "password": encrypted_password,
        }
        save_vault(self.vault)
        print(f"Added {site} to the vault.")

    def view_entries(self):
        if not self.vault:
            print("No entries found in the vault.")
            return

        for site, entry in self.vault.items():
            if isinstance(entry, dict):
                username = entry.get("username", "")
                password = entry.get("password", "")
                if self.fernet and isinstance(password, str):
                    try:
                        password = self.fernet.decrypt(password.encode("utf-8")).decode("utf-8")
                    except Exception:
                        pass
                print(f"{site}: {username} / {password}")


def main():
    print("Welcome to the Safe For Secrets")
    manager = PasswordManager()

    if manager.vault:
        print("Loaded entries from vault.json:")
        manager.view_entries()
    else:
        print("No vault data found yet. You can create one now.")

    while True:
        print("\nOptions:")
        print("1) Set master password")
        print("2) Add entry")
        print("3) View entries")
        print("4) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            master = create_master_password()
            manager.set_master_password(master)
        elif choice == "2":
            if not manager.fernet:
                print("Set a master password first.")
                continue
            site = input("Site name: ").strip()
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            manager.add_entry(site, username, password)
        elif choice == "3":
            manager.view_entries()
        elif choice == "4":
            print("Wrapping it up. Goodbye!")
            break
        else:
            print("You sure? Try again.")


if __name__ == "__main__":
    main()

