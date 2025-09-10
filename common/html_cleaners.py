import re
from bs4 import BeautifulSoup


def clean_urls(body_str):
    # Turn absolute URLs for internal biography links into relative URLs
    # e.g. https://www.falklandsbiographies.org/biographies/some
    # This happens as a result of copying and pasting from other web pages in
    # the browser when creating the links.

    soup = BeautifulSoup(body_str, "html.parser")
    links = soup.find_all("a")
    for link in links:
        if not link.has_attr("href"):
            # malformed link, skip it
            continue

        if not link["href"].startswith("http"):
            # already a relative link, skip it
            continue

        if "falklandsbiographies.org/biographies/" not in link["href"]:
            # not an internal biography link
            continue

        clean_link = re.sub(r"http[s]?://[^\/]+", "", link["href"])
        link["href"] = clean_link

        # We previously checked that the link was valid here, but that
        # there was no way to feed that back to the user, so better to just
        # clean the URL and let the weekly scan pick up any internal broken links.

    return str(soup)
