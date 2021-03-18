from cryptography.fernet import Fernet

def encrypt_fernet(message):
    key = "oRBCmPp9gPNBT_7uDilWwg1bEFwNd4jQBJiiKE9ClKA="
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())

    return encrypted_message

def decrypt_fernet(encrypted_message):
    key = "oRBCmPp9gPNBT_7uDilWwg1bEFwNd4jQBJiiKE9ClKA="
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message)

    return decrypted_message.decode()