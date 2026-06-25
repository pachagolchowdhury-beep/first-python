import os
import shutil


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def organize_files():
    source_folder = r"C:\Users\BISWAS\Downloads\snake"

    if not os.path.exists(source_folder):
        print("Source folder not found")
        return

    clear_screen()
    print("Scanning:", source_folder)

    for folder_name in ["png", "pdf", "html"]:
        folder_path = os.path.join(source_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    for name in os.listdir(source_folder):
        full_path = os.path.join(source_folder, name)

        if not os.path.isfile(full_path):
            continue

        if name.endswith(".png"):
            target_folder = os.path.join(source_folder, "png")
        elif name.endswith(".pdf"):
            target_folder = os.path.join(source_folder, "pdf")
        elif name.endswith(".html"):
            target_folder = os.path.join(source_folder, "html")
        else:
            continue

        destination = os.path.join(target_folder, name)
        if os.path.exists(destination):
            continue

        shutil.copy2(full_path, destination)
        print("Copied:", name)


if __name__ == "__main__":
    organize_files()
                                                    