from cryptography.fernet import Fernet
import os

MASTER_KEY = os.getenv("MASTER_KEY")

cipher = Fernet(MASTER_KEY)

def encrypt(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher.decrypt(data.encode()).decode()