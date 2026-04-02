import random
import string

def generate_short_id(length=7):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    short_id = ''.join(random.choice(characters) for _ in range(length))
    return short_id