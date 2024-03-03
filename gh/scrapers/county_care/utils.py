import random
import time
# import requests
from urllib.parse import urlparse

ALLOWED_DOMAINS = ("https://countycare",)

REQUEST_DELAY = 3

HEADERS1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
HEADERS2 = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
USER_AGENTS = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"]

def make_post(url, dictionary):
    """
    Make a request to `url` and return the raw response.

    This function ensure that the domain matches what is expected and that the rate limit
    is obeyed.
    """
    
    delay = REQUEST_DELAY + round(5*(random.random()), 2)
    index = random.randrange(0,5,1)
    headers = {'User-Agent': USER_AGENTS[index]}


    # check if URL starts with an allowed domain name
    for domain in ALLOWED_DOMAINS:
        if url.startswith(domain):
            break
    else:
        raise ValueError(f"can not fetch {url}, must be in {ALLOWED_DOMAINS}")
    time.sleep(delay)
    print(f"Fetching {url}")
    

    r = requests.post(url, json=dictionary, headers=headers)
    
    return r

def make_request(url):
    """
    Make a request to `url` and return the raw response.

    This function ensure that the domain matches what is expected and that the rate limit
    is obeyed.
    """
    # check if URL starts with an allowed domain name
    for domain in ALLOWED_DOMAINS:
        if url.startswith(domain):
            break
    else:
        raise ValueError(f"can not fetch {url}, must be in {ALLOWED_DOMAINS}")
    time.sleep(REQUEST_DELAY)
    print(f"Fetching {url}")
    resp = requests.get(url)
    return resp


def make_link_absolute(rel_url, current_url):
    """
    Given a relative URL like "/abc/def" or "?page=2"
    and a complete URL like "https://example.com/1/2/3" this function will
    combine the two yielding a URL like "https://example.com/abc/def"

    Parameters:
        * rel_url:      a URL or fragment
        * current_url:  a complete URL used to make the request that contained a link to rel_url

    Returns:
        A full URL with protocol & domain that refers to rel_url.
    """
    url = urlparse(current_url)
    if rel_url.startswith("/"):
        return f"{url.scheme}://{url.netloc}{rel_url}"
    elif rel_url.startswith("?"):
        return f"{url.scheme}://{url.netloc}{url.path}{rel_url}"
    else:
        return rel_url
