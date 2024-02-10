import sys
from scraper.twitter_scraper import Twitter_Scraper


def main(
        scraper: Twitter_Scraper = None,
        tweets: int = 50,
        username: str = None,
        hashtag: str = None,
        query: str = None,
        add: str = "",
        latest: bool = False,
        top: bool = False,
):
    try:

        additional_data: list = add.split(",")

        if not (username or hashtag or query):
            print("Please specify only one of --username, --hashtag, or --query.")
            sys.exit(1)

        if latest and top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        scraper.scrape_tweets(
            max_tweets=tweets,
            scrape_username=username,
            scrape_hashtag=hashtag,
            scrape_query=query,
            scrape_latest=latest,
            scrape_top=top,
            scrape_poster_details="pd" in additional_data,
        )
        scraper.save_to_csv()

    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
