#!/usr/bin/env python3
""" Auth File """


from ast import Bytes
import email

def _hash_password(password: str) -> str:
    """ Takes a password string arguments and 
    returns bytes"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
