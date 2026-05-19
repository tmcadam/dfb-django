import re
import requests
import concurrent.futures
from .models import Biography


def extract_urls(text):
    if not text:
        return []
    # simple regex for href attr
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', text)
    return urls


def check_link(url, bio):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400:
            return {"url": url, "bio": bio, "error": response.status_code}
    except requests.RequestException as e:
        return {"url": url, "bio": bio, "error": str(e)}
    return None


def check_links_in_bios():
    bios = Biography.objects.exclude(external_links__exact="")
    urls_to_check = []

    for bio in bios:
        urls = extract_urls(bio.external_links)
        for url in urls:
            if url.startswith("http"):
                urls_to_check.append((url, bio))

    fails = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(check_link, url, bio): (url, bio)
            for url, bio in urls_to_check
        }
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                fails.append(result)

    return {"fails": fails, "count": len(urls_to_check)}
