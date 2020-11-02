import scraper
import db

def run(url):
    details = scraper.get_product_details(url)
    result = ""
    if details is None:
        result = "not done"
    else:
        inserted = db.add_product_detail(details)
        print(details)
        if inserted:
            result = "done"
        else:
            result = "not done"
    return result


if __name__ == '__main__':
    URL = "https://www.amazon.de/dp/B08C5HYHYB/"

    print(run(URL))



