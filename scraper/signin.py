from scraper.twitter_scraper import Twitter_Scraper


def signin(username, password):
    scraper = Twitter_Scraper(
        username=username,
        password=password,
    )
    scraper.login()
    return scraper
