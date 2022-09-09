# This is a sample Python script.
from haiku_scrape import YoutubeScrape
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper = YoutubeScrape("https://old.reddit.com/r/youtubehaiku/top/?sort=top", 'month', 100)
    links = scraper.get_links_for_period()
    for link in links:
        print(link)


