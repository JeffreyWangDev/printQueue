import hashlib

def hash(string):
    return str(hashlib.sha256(string.encode()).hexdigest())