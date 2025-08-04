import string
import random
from urllib.parse import urlparse

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc != ''
