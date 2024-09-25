import re

def clean_urls(body_str):
    return re.sub(r"http[s]?://[^\/]+", "", body_str)