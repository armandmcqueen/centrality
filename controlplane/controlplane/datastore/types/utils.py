import uuid


def gen_random_uuid() -> str:
    """ Generate a random UUID as a string"""
    return str(uuid.uuid4())