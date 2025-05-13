import os
from cryptography.fernet import Fernet


def fetch_encryption_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()


def unlock_file(file_path, key):
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as f:
            f.write(decrypted_data)
        print(f"Decrypted the file: {file_path}")
    except Exception as e:
        print(f"Error decrypting the file: {file_path}: {e}")


def unlock_directory(target_path, key):
    for root, _, files in os.walk(target_path):
        for file in files:
            file_path = os.path.join(root, file)
            unlock_file(file_path, key)


if __name__ == "__main__":
    folder_to_decrypt = "critical"

    if not os.path.exists("secret.key"):
        print("[Trouble finding the secret Key, Cannot perform Decryption")
        exit()

    if not os.path.exists(folder_to_decrypt):
        print(f"Dir '{folder_to_decrypt}' does not exist.")
        exit()

    key = fetch_encryption_key()
    print(f"Decrypting folder: {folder_to_decrypt}")
    unlock_directory(folder_to_decrypt, key)
    print("\nAll files decrypted successfully, Thanks for the Ransom :p")
