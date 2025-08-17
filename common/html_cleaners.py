import re
from bs4 import BeautifulSoup
from django.urls import resolve, Resolver404


def clean_urls(body_str):
    soup = BeautifulSoup(body_str, "html.parser")
    links = soup.find_all("a")
    for link in links:
        if not link.has_attr("href"):
            continue
        clean_link = re.sub(r"http[s]?://[^\/]+", "", link["href"])
        try:
            resolve(clean_link)
            link["href"] = clean_link
        except Resolver404:
            # doesn't match an internal url, likely external or broken
            pass
    return str(soup)
