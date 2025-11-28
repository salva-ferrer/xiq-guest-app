
import random
def generate_password(length=8):
    return ''.join(str(random.randint(0,9)) for _ in range(length))
