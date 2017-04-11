#!/usr/bin/python

"""
Use Bing! to search news headlines.
"""


import argparse
import pprint
import random
import time
import webbrowser
import requests

SEARCH_MAX = 32
BING_URL = "https://www.bing.com/"
SEARCH_URL = "https://www.bing.com/search?q="

API_URL = "https://newsapi.org/v1/articles?apiKey="
API_SRC = "&source="
API_KEY = None

WBROWSER = None

NEWS_SOURCES = [
    "abc-news-au",
    "ars-technica",
    "associated-press",
    "bbc-news",
    "bbc-sport",
    "bloomberg",
    "cnbc",
    "cnn",
    "engadget",
    "espn",
    "espn-cric-info",
    "fortune",
    "google-news",
    "hacker-news",
    "independent",
    "national-geographic",
    "new-york-magazine",
    "recode",
    "reddit-r-all",
    "sky-news",
    "sky-sports-news",
    "techcrunch",
    "the-economist",
    "the-guardian-uk",
    "the-hindu",
    "the-new-york-times",
]

def __parse_args():
    parser = argparse.ArgumentParser("Bing! few news headlines.")

    parser.add_argument("searches", type=int, nargs='?', default=4,
                        help="number of Bing!s to be done, default=4")
    parser.add_argument("-k", "--key", type=str, required=True,
                        help="NewsAPI key")
    parser.add_argument("-b", "--browser", type=str, required=False,
                        help="browser to use, e.g., chrome, safari")
    return parser.parse_args()


def __news_get(source):
    news_url = API_URL + API_KEY + API_SRC + source

    try:
        print news_url
        resp = requests.get(news_url)
    except requests.exceptions.RequestException:
        print "Fetching news feeds failed."

    news_data = resp.json()
    if news_data['status'] == 'error':
        raise ValueError(news_data['message'])

    return news_data['articles']


def __news_desc_get(source):
    news = __news_get(source)

    if news is None:
        return None

    news_headlines = []
    for each_article in news:
        news_headlines.append(each_article['description'])

    return news_headlines


def bing_search(search_query):
    """ Do a Bing! search on the incoming query. """
    search_query = search_query.encode(encoding="utf-8")
    query = SEARCH_URL + str(search_query).replace(" ", "%20")
    WBROWSER.open_new_tab(query)
    print query


def do_bing_search(num_searches, browser):
    """ Do 'n' Bing! searches on a random news articles. """
    global WBROWSER

    if num_searches == 0:
        return

    if browser is None:
        try:
            WBROWSER = webbrowser.get()
        except webbrowser.Error:
            print "Error: No browsers found."
            exit (-1)
    elif:
        try:
            WBROWSER = webbrowser.get(browser)
        except webbrowser.Error:
            print "Error: Browser '%s' not found." % (browser)
            exit (-1)

    WBROWSER.open(BING_URL, new=1, autoraise=True)
    while num_searches:
        news_src = random.choice(NEWS_SOURCES)

        news = __news_desc_get(news_src)
        if news is None:
            # Fetching news from that source failed. Try another source.
            continue

        for each_article in news:
            bing_search(each_article)

            num_searches -= 1
            if num_searches == 0:
                break

            time.sleep(2)


def main():
    global API_KEY

    args = __parse_args()
    API_KEY = args.key
    do_bing_search(int(args.searches), args.browser)


if __name__ == "__main__":
    main()
