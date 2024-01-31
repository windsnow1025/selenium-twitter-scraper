import os
import sys
import argparse
import getpass
from scraper.twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def main(
        tweets: int = 50,
        username: str = None,
        hashtag: str = None,
        query: str = None,
        add: str = "",
        latest: bool = False,
        top: bool = False,
):
    try:
        user = os.environ.get("TWITTER_USERNAME")
        password = os.environ.get("TWITTER_PASSWORD")

        USER_UNAME = user
        USER_PASSWORD = password

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        print()

        tweet_type_args = []

        if username is not None:
            tweet_type_args.append(username)
        if hashtag is not None:
            tweet_type_args.append(hashtag)
        if query is not None:
            tweet_type_args.append(query)

        additional_data: list = add.split(",")

        if len(tweet_type_args) > 1:
            print("Please specify only one of --username, --hashtag, or --query.")
            sys.exit(1)

        if latest and top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(
                username=USER_UNAME,
                password=USER_PASSWORD,
            )
            scraper.login()
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
            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print(
                "Missing Twitter username or password environment variables. Please check your .env file."
            )
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    scraper.driver.quit()


if __name__ == "__main__":
    main()
