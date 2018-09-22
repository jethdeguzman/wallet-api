import bcrypt
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def encrypt_password(password):
    if not isinstance(password, str):
        raise TypeError('password should be string')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()
