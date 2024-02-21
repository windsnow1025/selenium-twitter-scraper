import sys

from scraper.twitter_scraper import Twitter_Scraper


def signin(username, password):
    if not username or not password:
        print("Please set your Twitter username and password in the environment variables.")
        sys.exit(1)

    scraper = Twitter_Scraper(
        username=username,
        password=password,
    )

    try:
        scraper.login()
    except Exception as e:
        scraper.driver.close()
        sys.exit(1)
    return scraper
