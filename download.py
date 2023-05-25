import os
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def download_recursive(url, directory, extension=".html"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    visited_urls = set()
    urls_to_visit = [url]

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        visited_urls.add(current_url)

        html_content = urllib.request.urlopen(current_url).read().decode("utf-8")
        links = extract_links(html_content)

        for link in links:
            absolute_url = urljoin(current_url, link)
            if absolute_url.endswith(extension) and absolute_url not in visited_urls:
                file_name = link.split("/")[-1]
                file_path = os.path.join(directory, file_name)
                urllib.request.urlretrieve(absolute_url, file_path)
                visited_urls.add(absolute_url)
            elif absolute_url.startswith(url) and absolute_url not in visited_urls:
                urls_to_visit.append(absolute_url)


def extract_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    return links


# Usage
download_recursive("https://python.langchain.com/en/latest/", "langchain-docs", ".html")
