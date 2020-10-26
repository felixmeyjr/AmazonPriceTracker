import requests
from bs4 import BeautifulSoup
import re


#@todo argparsing rather than function parameter itself?

def get_url(url):
    """
    Shortening the URL and verify a valid URL
    :param url: url
    :return: url
    """
    if url.find("www.amazon.de") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.de" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.de" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url


def get_price(price):
    #print(price)
    converted_price = re.sub(",", ".", price)
    converted_price = re.sub("\xa0", "", converted_price)
    converted_price = float(re.sub("€", "", converted_price))
    return converted_price


def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
    }
    details = {
        "name"  : "",
        "price" : 0,
        "deal"  : False,
        "url"   : ""
    }

    _url = get_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_ourprice")
        if price is None:
            price = soup.find(id="priceblock_dealprice")
            details["deal"] = True
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_price(price.get_text())
            details["url"] = _url
        else:
            print("Something went wrong")
            return None

    return details











