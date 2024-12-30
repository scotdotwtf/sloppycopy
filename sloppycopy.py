# sloppycopy v1.0 - cats <3
import os
import zlib
import shutil

# stat variable & func
total_changes = 0

def add_total():
    global total_changes
    total_changes += 1

# function to check files
def crc32(path):
    checksum = 0
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4069), b""):
            checksum = zlib.crc32(chunk, checksum)
    return checksum

# function to copy files
def copy(source_dir, target_dir):
    print("Adding & updating files & folders:")
    for root, _, files in os.walk(source_dir):
        target_root = os.path.join(target_dir, os.path.relpath(root, source_dir))
        
        if not os.path.exists(target_root):
            os.makedirs(target_root)
            print(f"Added folder: {target_root}")
            add_total()
        
        for file_name in files:
            source_file = os.path.join(root, file_name)
            target_file = os.path.join(target_root, file_name)

            if os.path.exists(target_file):
                if crc32(source_file) != crc32(target_file):
                    shutil.copy2(source_file, target_file)
                    print(f"Updated file: {source_file} -> {target_file}")
                    add_total()
            else:
                shutil.copy2(source_file, target_file)
                print(f"Added file: {source_file} -> {target_file}")
                add_total()

    print("Removing files & folders:")
    for root, directories, files in os.walk(target_dir):
        source_root = os.path.join(source_dir, os.path.relpath(root, target_dir))

        for file_name in files:
            if not os.path.exists(os.path.join(source_root, file_name)):
                os.remove(os.path.join(root, file_name))
                print(f"Removed file: {os.path.join(root, file_name)}")
                add_total()

        for dir_name in directories:
            if not os.path.exists(os.path.join(source_root, dir_name)):
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"Removed folder: {os.path.join(root, dir_name)}")
                add_total()

# simple cli program
if __name__ == "__main__":
    source_directory = input("Source directory path: ")
    target_directory = input("Target directory path: ")

    copy(source_directory, target_directory)
    print(f"Copying done, total changes: {total_changes}")