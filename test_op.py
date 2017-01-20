import random

def gen_phone():
    first = str(random.randint(1000000000,9999999999))

    return '{}-{}-{}'.format(first)