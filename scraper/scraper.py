import sys
from scraper.twitter_scraper import TwitterScraper


def scrape(
        scraper: TwitterScraper = None,
        tweets: int = 50,
        username: str = None,
        hashtag: str = None,
        query: str = None,
        add: str = "",
        latest: bool = False,
        top: bool = False,
        to_csv: bool = True
):
    additional_data: list = add.split(",")

    if not (username or hashtag or query):
        print("Please specify only one of username, hashtag, or query.")
        raise ValueError

    if latest and top:
        print("Please specify either latest or top. Not both.")
        raise ValueError

    scraper.scrape_tweets(
        max_tweets=tweets,
        scrape_username=username,
        scrape_hashtag=hashtag,
        scrape_query=query,
        scrape_latest=latest,
        scrape_top=top,
        scrape_poster_details="pd" in additional_data,
    )

    if to_csv:
        scraper.save_to_csv()

    return len(scraper.data)


def signin(username, password):
    if not username or not password:
        print("Please set your Twitter username and password in the environment variables.")
        sys.exit(1)

    scraper = TwitterScraper(
        username=username,
        password=password,
    )

    try:
        scraper.login()
    except:
        scraper.driver.close()
        return None

    return scraper
