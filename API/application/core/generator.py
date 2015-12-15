import random
import string

class Generator:

    @staticmethod
    def password(size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

